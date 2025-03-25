from django import forms
from apps.attendance_record.models import AttendanceRecord

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['employee', 'date', 'check_in', 'check_out', 'login_type']
        widgets = {
            'date': forms.DateInput(attrs={ 'type': 'date','class': 'form-control'}),
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            
        }
        
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                })


class ImportCSVForm(forms.Form):
    file = forms.FileField(required=True)
    