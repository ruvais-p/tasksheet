# Generated by Django 3.2.25 on 2025-07-13 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_timesheet_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_department_head',
        ),
        migrations.AddField(
            model_name='timesheet',
            name='department_head_remark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='employee_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=20, unique=True)),
                ('department', models.CharField(default='Unknown', max_length=100)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=20, unique=True)),
                ('department', models.CharField(default='Unknown', max_length=100)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='timesheet',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.employee'),
        ),
    ]
