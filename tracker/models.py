from django.contrib.auth.models import AbstractUser
from django.db import models

# Add this at the top of models.py
SUB_DEPARTMENT_CHOICES = {
    'ADM': [
        ('Sessional-Head', 'Sessional Head'),
        ('ADM-Research', 'ADM Research'),
        ('B-Employee', 'B Employee'),
    ],
    'SOE': [
        ('CSE', 'Department of Computer Science'),
        ('CE', 'Department of Civil'),
        ('ECE', 'Department of Electronics'),
        ('ME', 'Department of Mechanical'),
        ('EE', 'Department of Electrical'),
    ],
    'SLS': [
        ('xxxxx', 'xxxx'),
        ('yyyyy', 'yyyy'),
    ],
    # Add more departments and their sub-departments as needed
}

class User(AbstractUser):
    """Base user class for admin functionality"""
    is_admin = models.BooleanField(default=False)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

class Employee(models.Model):
    """Employee model for regular employees"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, default="Unknown")
    sub_department = models.CharField(max_length=100, blank=True, null=True)
    allocated_post = models.CharField(max_length=100, default="Unknown")
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"

class DepartmentHead(models.Model):
    """Department Head model for department heads"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, default="Unknown")
    sub_department = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.department} Head"

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

    # Link to Employee instead of User
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    week = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, default="Unknown") 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    work_description = models.CharField(max_length=50, choices=WORK_DESC_CHOICES)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_remark = models.TextField(blank=True, null=True)
    department_head_remark = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']