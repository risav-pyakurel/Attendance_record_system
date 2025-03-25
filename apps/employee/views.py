from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from mixins.mixins import EmployeePermissionMixin
from apps.employee.models import Employee
from apps.employee.forms import EmployeeForm, EmployeeLoginForm, PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm



class EmployeeListView(LoginRequiredMixin, EmployeePermissionMixin, ListView):
    model = Employee
    template_name = 'employee/list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='employee').exists():
            queryset = queryset.filter(id=self.request.user.id)
        return queryset

            

    

class EmployeeCreateView(LoginRequiredMixin,EmployeePermissionMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/form.html'
    success_url = reverse_lazy('employee:employee_list')
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='employee').exists():
            queryset = queryset.filter(id=self.request.user.id)
        return queryset



class EmployeeUpdateView(LoginRequiredMixin,EmployeePermissionMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/form.html'
    success_url = reverse_lazy('employee:employee_list')
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='employee').exists():
            queryset = queryset.filter(id=self.request.user.id)
        return queryset



class EmployeeDeleteView(LoginRequiredMixin,EmployeePermissionMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employee:employee_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, 'Employee deleted successfully.')
            return response
        except Exception:
            messages.error(self.request, 'Sorry, this employee cannot be deleted.')
            return redirect('employee:employee_list')
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='employee').exists():
            queryset = queryset.filter(id=self.request.user.id)
        return queryset




class EmployeeLogin(LoginView):
    form_class = EmployeeLoginForm
    template_name = 'employee/login.html'
    success_url = reverse_lazy('attendance_record:attendance_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(self.success_url)
                else:
                    messages.error(request, "This account is inactive")
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid form data")
        return render(request, self.template_name, {'form': form})



class EmployeePasswordResetView(SuccessMessageMixin, FormView):
    template_name = 'employee/password_reset.html'
    success_url = reverse_lazy('employee:password_reset_done')
    form_class = PasswordResetForm
    success_message = "Password reset email has been sent successfully."

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            messages.error(self.request, "No account found with this email address.")
            return self.form_invalid(form)

        token = default_token_generator.make_token(employee)
        reset_url = self.request.build_absolute_uri(
            reverse('employee:password_reset_confirm', kwargs={
                'pk': employee.pk,
                'token': token
            })
        )

        send_mail(
            subject='Password Reset Request',
            message=f"""
            You requested to reset your password.
            Please click the following link to reset your password:
            {reset_url}

            If you did not request this reset, please ignore this email.
            Sincerely,
            Bottle
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return super().form_valid(form)
    

class EmployeePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'employee/password_change.html'
    success_url = reverse_lazy('employee:password_change_done')
    success_message = "Your password has been updated successfully."

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            update_session_auth_hash(self.request, form.user)
            messages.success(self.request, self.success_message)
            return response
        except Exception as e:
            raise e


class EmployeePasswordResetConfirmView(SuccessMessageMixin, FormView):
    template_name = 'employee/password_change.html'
    success_url = reverse_lazy('employee:login')
    form_class = SetPasswordForm
    success_message = "Your password has been reset successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_user(self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['token'] = self.kwargs['token']
        return context

    def form_valid(self, form):
        user = self.get_user(self.kwargs['pk'])
        token = self.kwargs['token']

        if default_token_generator.check_token(user, token):
            form.save()
            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid or expired password reset link. Please request a new reset.")
            return redirect('employee:password_reset')

    def get_user(self, pk):
        return get_object_or_404(Employee, pk=pk)


class EmployeePasswordResetDoneView(TemplateView):
    template_name = 'employee/password_reset_done.html'


