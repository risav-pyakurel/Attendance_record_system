from django.db import models
from apps.employee.models import Employee
from apps.common.models import BaseModel
from utils.datetime_utils import get_time_difference
from datetime import datetime


class AttendanceRecord(BaseModel):
    CHOICES= (
        ('RM', 'Remote'),
        ('OS', 'On-Site'),
        ('HR', 'Hybrid'),
    )
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT)
    date = models.DateField(null=True, blank= True)
    check_in = models.DateTimeField(null=True, blank= True)
    check_out = models.DateTimeField(null=True, blank= True)
    record_time = models.DateTimeField(null=True)
    login_type = models.CharField(choices= CHOICES, max_length=2)
    work_hour = models.DecimalField(max_digits=5, decimal_places=1, null= True, blank = True)
    
    def __str__(self) -> str:
        return f"{self.employee}"
    
    
    def save(self, *args, **kwargs):
        if self.check_out is not None:
            self.work_hour = get_time_difference(self.check_in, self.check_out)
            
        else:
            self.work_hour = 0
        
        super().save(*args, **kwargs)
            
