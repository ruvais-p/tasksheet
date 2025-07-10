from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    employee_id = models.CharField(max_length=20, unique=True)

class Timesheet(models.Model):
    CATEGORY_CHOICES = [
        ('Teaching', 'Teaching'),
        ('Adm work', 'Administration Work'),
        ('Project', 'Project'),
        ('Research', 'Research'),
        # Add more as required
    ]
    WORK_DESC_CHOICES = [
        ('Lecture', 'Lecture'),
        ('Lab', 'Lab'),
        ('Exam duty', 'Exam Duty'),
        ('Paper valuation', 'Paper Valuation'),
        ('QP setting', 'QP Setting'),
        ('Outreach', 'Outreach Activities'),
        ('PG-PhD research', 'PG-PhD Research Discussion'),
        ('Valuation', 'Valuation'),
        # Add more as required
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rework', 'Rework'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.DateField()  # Could be a week start date
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    work_description = models.CharField(max_length=50, choices=WORK_DESC_CHOICES)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_remark = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']