from django.urls import path
from apps.attendance_record.views import (
    AttendanceRecordListView, AttendanceRecordCreateView, AttendanceRecordUpdateView, 
    AttendanceRecordDeleteView, ImportCSVView
)

app_name = 'attendance_record'

urlpatterns = [
    path('attendance-record/', AttendanceRecordListView.as_view(), name='attendance_list'),
    path('attendance-record/create/', AttendanceRecordCreateView.as_view(), name='attendance_create'),
    path('attendance-record/update/<int:pk>', AttendanceRecordUpdateView.as_view(), name='attendance_update'),
    path('attendance-record/delete/<int:pk>', AttendanceRecordDeleteView.as_view(), name='attendance_delete'),
    path('attendance-record/import', ImportCSVView.as_view(), name='attendance_import'),
]
