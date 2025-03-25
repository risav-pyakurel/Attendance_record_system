from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class EmployeeManager(BaseUserManager):
    def create_employee(self,email,password,**extrafields):
        if not email:
            raise ValueError(_('Email must be set'))
        email = self.normalize_email(email)
        employee = self.model(email=email, **extrafields)
        employee.set_password(password)
        employee.save()
        return employee

    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_employee(email, password, **extra_fields)