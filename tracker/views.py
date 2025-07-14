from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import AllocatedPost, PostDuty, TimesheetEntry, User, Employee, DepartmentHead, Timesheet
from .forms import (
    EmployeePostAllocationForm, EmployeeSignUpForm, EmployeeSignInForm, 
    DepartmentHeadSignUpForm, DepartmentHeadSignInForm, TimesheetForm
)

# Employee Views
def employee_signup_view(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_signin')
    else:
        form = EmployeeSignUpForm()
    return render(request, 'employee_signup.html', {'form': form})

@csrf_exempt
def employee_signin_view(request):
    if request.method == 'POST':
        form = EmployeeSignInForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            password = form.cleaned_data.get('password')
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                user = authenticate(request, username=employee.user.username, password=password)
                
                if user is not None:
                    if employee.allocated_post is None:
                        form.add_error(None, "Your profile is under processing. Please contact your department head.")
                    else:
                        login(request, user)
                        return redirect('employee_dashboard')
                else:
                    form.add_error(None, "Invalid employee ID or password")
            except Employee.DoesNotExist:
                form.add_error(None, "Invalid employee ID or password")
    else:
        form = EmployeeSignInForm()
    
    return render(request, 'employee_signin.html', {'form': form})

@csrf_exempt
def employee_dashboard(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('employee_signin')
    
    if request.method == 'POST':
        form = TimesheetForm(request.POST, employee=employee)
        if form.is_valid():
            # Create Timesheet
            timesheet = Timesheet.objects.create(
                employee=employee,
                date=form.cleaned_data['date'],
                department=employee.department,
                status='Submitted'
            )
            
            # Create Timesheet entries
            for duty in employee.allocated_post.duties.all():
                hours = form.cleaned_data.get(f'duty_{duty.id}')
                if hours and float(hours) > 0:
                    TimesheetEntry.objects.create(
                        timesheet=timesheet,
                        duty=duty,
                        hours=hours
                    )
            
            return redirect('employee_dashboard')
    else:
        form = TimesheetForm(employee=employee)
    
    # Get previous timesheets
    previous_timesheets = Timesheet.objects.filter(employee=employee).prefetch_related('entries')
    
    return render(request, 'employee_dashboard.html', {
        'form': form,
        'previous_timesheets': previous_timesheets,
        'employee': employee,
    })
# Department Head Views
def department_head_signup_view(request):
    if request.method == 'POST':
        form = DepartmentHeadSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_head_signin')
    else:
        form = DepartmentHeadSignUpForm()
    return render(request, 'department_head_signup.html', {'form': form})

def department_head_signin_view(request):
    if request.method == 'POST':
        form = DepartmentHeadSignInForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            password = form.cleaned_data.get('password')
            try:
                dept_head = DepartmentHead.objects.get(employee_id=employee_id)
                user = authenticate(request, username=dept_head.user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('department_head_dashboard')
            except DepartmentHead.DoesNotExist:
                form.add_error(None, "Invalid employee ID or password")
    else:
        form = DepartmentHeadSignInForm()
    return render(request, 'department_head_signin.html', {'form': form})

@csrf_exempt
def department_head_dashboard(request):
    try:
        dept_head = DepartmentHead.objects.get(user=request.user)
    except DepartmentHead.DoesNotExist:
        return redirect('department_head_signin')
    
    selected_employee = None
    employee_timesheets = []
    
    # Handle form submissions
    if request.method == 'POST':
        # Existing timesheet approval handling
        ts_id = request.POST.get('ts_id')
        action = request.POST.get('action')
        remark = request.POST.get('department_head_remark', '')
        
        # Post allocation handling
        employee_id = request.POST.get('employee_id')
        allocated_post_id = request.POST.get('allocated_post')
        
        # New post handling
        new_post_name = request.POST.get('new_post_name')
        new_post_description = request.POST.get('new_post_description')
        
        # New duty handling
        new_duty_post_id = request.POST.get('new_duty_post')
        new_duty_name = request.POST.get('new_duty_name')
        new_duty_description = request.POST.get('new_duty_description')
        
        if ts_id and action in ['Approved', 'Rejected', 'Rework']:
            try:
                timesheet = Timesheet.objects.get(id=ts_id, department=dept_head.department)
                timesheet.status = action
                timesheet.department_head_remark = remark
                timesheet.save()
            except Timesheet.DoesNotExist:
                pass
        
        if employee_id and allocated_post_id:
            try:
                employee = Employee.objects.get(employee_id=employee_id, department=dept_head.department)
                post = AllocatedPost.objects.get(id=allocated_post_id)
                employee.allocated_post = post
                employee.save()
                selected_employee = employee
            except (Employee.DoesNotExist, AllocatedPost.DoesNotExist):
                pass
                
        if new_post_name:
            post = AllocatedPost.objects.create(
                department=dept_head.department,
                sub_department=dept_head.sub_department,
                post_name=new_post_name,
                description=new_post_description,
                created_by=dept_head
            )
        
        if new_duty_post_id and new_duty_name:
            try:
                post = AllocatedPost.objects.get(id=new_duty_post_id)
                PostDuty.objects.create(
                    post=post,
                    duty_name=new_duty_name,
                    description=new_duty_description
                )
            except AllocatedPost.DoesNotExist:
                pass
    
    # Get department employees
    department_employees = Employee.objects.filter(department=dept_head.department)
    
    # Get selected employee if specified
    employee_id = request.GET.get('employee_id')
    if employee_id:
        try:
            selected_employee = Employee.objects.get(employee_id=employee_id, department=dept_head.department)
            employee_timesheets = Timesheet.objects.filter(employee=selected_employee).order_by('-submitted_at')
        except Employee.DoesNotExist:
            pass
    
    # Get posts and duties for this department
    department_posts = AllocatedPost.objects.filter(department=dept_head.department)
    if dept_head.sub_department:
        department_posts = department_posts.filter(sub_department=dept_head.sub_department)
    
    # Get statistics for right panel
    pending_timesheets = Timesheet.objects.filter(
        department=dept_head.department,
        status__in=['Open', 'Submitted', 'Rework']
    )
    approved_timesheets = Timesheet.objects.filter(
        department=dept_head.department,
        status='Approved'
    )
    
    return render(request, 'department_head_dashboard.html', {
        'department_employees': department_employees,
        'selected_employee': selected_employee,
        'employee_timesheets': employee_timesheets,
        'pending_timesheets': pending_timesheets,
        'approved_timesheets': approved_timesheets,
        'department': dept_head.department,
        'sub_department': dept_head.sub_department,
        'employee_name': dept_head.user.username,
        'dept_head': dept_head,
        'department_posts': department_posts,
    })
@csrf_exempt  # Only for testing! Use csrf_token in your template in production.
def admin_dashboard(request):
    # Check if user is admin
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('admin_signin')
    
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

# Admin signin (you'll need to create this view and template)
def admin_signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_admin:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'admin_signin.html')

# Legacy views for backward compatibility (redirect to new views)
def signup_view(request):
    return redirect('employee_signup')

def signin_view(request):
    return redirect('employee_signin')