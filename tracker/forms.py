from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Timesheet

class SignUpForm(UserCreationForm):
    employee_id = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['employee_id', 'username', 'password1', 'password2']

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