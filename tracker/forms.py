from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Timesheet

DEPARTMENT_CHOICES = [
    ('CSE', 'Computer Science'),
    ('ECE', 'Electronics'),
    ('ME', 'Mechanical'),
    ('CE', 'Civil'),
    ('EE', 'Electrical'),
    # Add more as needed
]

class SignUpForm(UserCreationForm):
    employee_id = forms.CharField(max_length=20)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)  # Added department selection

    class Meta:
        model = User
        fields = ['employee_id', 'department', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.employee_id = self.cleaned_data['employee_id']
        user.department = self.cleaned_data['department']
        if commit:
            user.save()
        return user

class SignInForm(forms.Form):
    employee_id = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    
class TimesheetEntryForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['category', 'work_description', 'date', 'hours']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'category': forms.Select(),
            'work_description': forms.Select(),
            'hours': forms.NumberInput(attrs={'step': '0.25'}),
        }
        
class DepartmentHeadSignUpForm(UserCreationForm):
    employee_id = forms.CharField(max_length=20)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)

    class Meta:
        model = User
        fields = ['employee_id', 'department', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.employee_id = self.cleaned_data['employee_id']
        user.department = self.cleaned_data['department']
        user.is_department_head = True  # Mark as department head
        if commit:
            user.save()
        return user

class DepartmentHeadSignInForm(forms.Form):
    employee_id = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)