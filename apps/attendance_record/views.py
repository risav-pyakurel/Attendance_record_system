from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from django.utils.timezone import make_aware
from io import TextIOWrapper
import csv
from datetime import datetime

from apps.attendance_record.models import AttendanceRecord
from apps.attendance_record.forms import AttendanceRecordForm, ImportCSVForm
from apps.employee.models import Employee
from mixins.mixins import AttendancePermissionMixins
from utils.datetime_utils import parse_custom_time_format


class AttendanceRecordListView(LoginRequiredMixin, AttendancePermissionMixins,ListView):
    model = AttendanceRecord
    template_name = 'attendance_record/list.html'
    context_object_name = 'attendance_records'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='employee').exists():
            queryset = queryset.filter(id=self.request.user.id)
    
    
        queryset = queryset.order_by('-updated_at')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(employee__first_name__icontains=search_query) |
                Q(employee__last_name__icontains=search_query) |
                Q(login_type__icontains=search_query) |
                Q(check_in__icontains=search_query) |
                Q(check_out__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class AttendanceRecordCreateView(LoginRequiredMixin, AttendancePermissionMixins,CreateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = 'attendance_record/form.html'
    success_url = reverse_lazy('attendance_record:attendance_list')
    success_message = 'Attendance Created Sucessfully'


class AttendanceRecordUpdateView(LoginRequiredMixin,AttendancePermissionMixins, UpdateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = 'attendance_record/form.html'
    success_url = reverse_lazy('attendance_record:attendance_list')
    success_message = 'Attendance record successfully updated'
    

class AttendanceRecordDeleteView(LoginRequiredMixin,AttendancePermissionMixins, DeleteView):
    model = AttendanceRecord
    template_name = 'attendance_record/confirm_delete.html'
    success_url = reverse_lazy('attendance_record:attendance_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Attendance record deleted successfully.')
        return super().delete(request, *args, **kwargs)


class ImportCSVView(LoginRequiredMixin,AttendancePermissionMixins, FormView):
    form_class = ImportCSVForm
    template_name = 'attendance_record/import_csv.html'
    success_url = reverse_lazy('attendance_record:attendance_list')

    def get_date_from_filename(self, filename):
        try:
            date_str = filename.replace('.csv', '')
            return datetime.strptime(date_str, '%d-%m-%Y')
        except Exception as e:
            raise ValueError(f"Invalid filename format. Expected DD-MM-YYYY.csv, got {filename}") from e

    def process_time_entries(self, entries, attendance_date):
        try:
            if not entries:
                return None, None
            entries = [entry.time() if isinstance(entry, datetime) else entry for entry in entries]
            entries.sort()
            check_in = entries[0]
            check_out = entries[-1]
            check_in_datetime = datetime.combine(attendance_date.date(), check_in)
            check_out_datetime = datetime.combine(attendance_date.date(), check_out)

            check_in_datetime = make_aware(check_in_datetime) if timezone.is_naive(check_in_datetime) else check_in_datetime
            check_out_datetime = make_aware(check_out_datetime) if timezone.is_naive(check_out_datetime) else check_out_datetime

            return check_in_datetime, check_out_datetime
        except Exception as e:
            raise ValueError(f"Exception processing time entries: {e}")
           

    def form_valid(self, form):
        csv_file = form.cleaned_data['file']
        try:
            attendance_date = self.get_date_from_filename(csv_file.name)
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        existing_records = AttendanceRecord.objects.filter(record_time__date=attendance_date.date()).delete()
        decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
        csv_reader = csv.reader(decoded_file)

        daily_records = {}

        for row in csv_reader:
            try:
                line = ' '.join(row).strip()
                if not line:
                    continue
                parts = line.strip("'").split()
                if len(parts) < 3:
                    continue
                user_id = int(parts[0])
                time = parts[-1]
                name = ' '.join(parts[1:-1])

                if user_id not in daily_records:
                    daily_records[user_id] = []
                daily_records[user_id].append(parse_custom_time_format(time))

            except Exception as e:
                print(f"Exception: {e} {row}")
                messages.error(self.request, f'Error processing row: {row}. Error: {str(e)}')
                
        for user_id, times in daily_records.items():
            try:
                check_in_datetime, check_out_datetime = self.process_time_entries(times, attendance_date)
                if check_in_datetime and check_out_datetime:
                    with transaction.atomic():
                        try:
                            employee = Employee.objects.get(device_id=user_id)
                            AttendanceRecord.objects.create(
                                employee= employee,
                                check_in=check_in_datetime,
                                check_out=check_out_datetime,
                                record_time=check_in_datetime,
                                login_type='OS',
                            )
                        except Exception as e:
                            print("Employee not found", e)
            except Exception as e:
                messages.error(self.request, f'Error creating attendance record for employee {user_id}: {str(e)}')

        messages.success(self.request, 'CSV file imported successfully.')
        return super().form_valid(form)

