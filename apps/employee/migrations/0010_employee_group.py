# Generated by Django 5.1.2 on 2024-11-27 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_rename_group_employee_designation'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='group',
            field=models.CharField(blank=True, choices=[('AD', 'Admin'), ('EMP', 'Employee')], null=True),
        ),
    ]
