from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('dashboard/', views.employee_dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]