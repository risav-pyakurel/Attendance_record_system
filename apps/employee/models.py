from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.employee.manager import EmployeeManager



class Employee(AbstractBaseUser, PermissionsMixin):
    DESIGNATION = (
        ('BP',"Bottle Payments"),
        ("DS", "Designer"),
        ("DV", "Developer"),
        ("MR", "Manager"),
        ("OA", "Office Admin"),
        ("QA","Quality Assurance")
    )
    GROUPS = (
        ('AD', "Admin"),
        ('EMP', "Employee")
    )
    
    redmine_id = models.CharField(max_length=255, unique= True, null=True, blank=True)
    device_id = models.IntegerField(unique= True, null=True, blank=True)
    first_name = models.CharField( max_length=150, blank=True)
    last_name = models.CharField( max_length=150, blank=True)
    email = models.EmailField(unique=True, max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    designation = models.CharField(choices=DESIGNATION, max_length=3, null=True, blank = True)
    group = models.CharField(choices=GROUPS,null=True,blank=True)

        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = EmployeeManager()
    
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    
    def __str__(self) -> str:
        return f"{self.email}"
    

