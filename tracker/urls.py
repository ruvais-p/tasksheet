from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Employee URLs
    path('employee/signup/', views.employee_signup_view, name='employee_signup'),
    path('employee/signin/', views.employee_signin_view, name='employee_signin'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    
    # Department Head URLs
    path('department-head/signup/', views.department_head_signup_view, name='department_head_signup'),
    path('department-head/signin/', views.department_head_signin_view, name='department_head_signin'),
    path('department-head/dashboard/', views.department_head_dashboard, name='department_head_dashboard'),
    
    # Admin URLs
    path('admin/signin/', views.admin_signin_view, name='admin_signin'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Legacy URLs (for backward compatibility)
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('dashboard/', views.employee_dashboard, name='dashboard'),
    
    # Logout
    path('logout/', LogoutView.as_view(next_page='employee_signin'), name='logout'),
]