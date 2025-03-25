from django.urls import path
from django.views.generic import RedirectView

from apps.employee.views import (
    EmployeeListView, 
    EmployeeCreateView, 
    EmployeeUpdateView, 
    EmployeeDeleteView,
    EmployeeLogin,
    EmployeePasswordResetView,
    EmployeePasswordChangeView,
    EmployeePasswordResetConfirmView,
    EmployeePasswordResetDoneView  
)

app_name = 'employee'

urlpatterns = [

    path('', RedirectView.as_view(url='/login/', permanent=False), name='home_redirect'),
    path('login/', EmployeeLogin.as_view(success_url='/dashboard/attendance/attendance-record/'), name='login'),
    path('password-reset/', EmployeePasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', EmployeePasswordResetDoneView.as_view(), name='password_reset_done'),  
    path('password-reset-confirm/<int:pk>/<str:token>/', EmployeePasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-change/', EmployeePasswordChangeView.as_view(), name='password_change'),
    path('employee-record/list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee-record/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee-record/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee-record/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
]
