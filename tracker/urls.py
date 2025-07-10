from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('dashboard/', views.employee_dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('department-head-signup/', views.department_head_signup_view, name='department_head_signup'),
    path('department-head-signin/', views.department_head_signin_view, name='department_head_signin'),
    path('department-head-dashboard/', views.department_head_dashboard, name='department_head_dashboard'),
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'),
]