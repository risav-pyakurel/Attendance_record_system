from django import forms
from apps.employee.models import Employee


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'date_joined', 'redmine_id', 'device_id', 'first_name', 
            'last_name', 'email', 'designation','group'
        ]
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
           
        }
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                })

class EmployeeLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }
        )
    )
    
class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )