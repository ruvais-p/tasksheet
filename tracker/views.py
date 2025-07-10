from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import User
from .forms import SignUpForm, SignInForm
from django.contrib.auth.decorators import login_required
from .models import Timesheet
from .forms import TimesheetEntryForm
from .models import Timesheet 


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            password = form.cleaned_data.get('password')
            try:
                user_obj = User.objects.get(employee_id=employee_id)
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
            except User.DoesNotExist:
                user = None  # Invalid login
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


@login_required
def employee_dashboard(request):
    user = request.user
    if request.method == 'POST':
        form = TimesheetEntryForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.user = user
            timesheet.department = user.department  # Set department from User
            timesheet.status = 'Submitted'
            timesheet.save()
            # Optionally, send notification to admin
    else:
        form = TimesheetEntryForm()
    previous_entries = Timesheet.objects.filter(user=user)
    return render(request, 'employee_dashboard.html', {
        'form': form,
        'previous_entries': previous_entries,
        'employee_name': user.username,
    })

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only for testing! Use csrf_token in your template in production.
def admin_dashboard(request):
    timesheets = Timesheet.objects.all().order_by('-submitted_at')

    if request.method == 'POST':
        ts_id = request.POST.get('ts_id')
        action = request.POST.get('action')  # 'Approved', 'Rejected', 'Rework'
        remark = request.POST.get('admin_remark', '')
        try:
            timesheet = Timesheet.objects.get(id=ts_id)
            if action in ['Approved', 'Rejected', 'Rework']:
                timesheet.status = action
                timesheet.admin_remark = remark
                timesheet.save()
        except Timesheet.DoesNotExist:
            pass  # handle error if needed

    return render(request, 'admin_dashboard.html', {'timesheets': timesheets})