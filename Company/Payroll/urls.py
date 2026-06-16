from django.urls import path
from .views import payroll_dashboard, manage_payroll

urlpatterns = [
    path('', payroll_dashboard, name='payroll_dashboard'),
    path('manage/', manage_payroll, name='manage_payroll'),
]
