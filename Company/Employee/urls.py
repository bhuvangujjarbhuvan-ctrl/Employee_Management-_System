from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name='home'),
    path('employee/add/', add_employee, name='employee_add'),
    path('employee/view/<int:emp_id>/', employee_detail, name='employee_detail'),
    path('employee/delete/<int:emp_id>/', delete_employee, name='employee_delete'),
    path('employee/edit/<int:emp_id>/', edit_employee, name='employee_edit'),
    path('employee/view/', employee_list, name='employee_list'),
    path('accounts/signup/', signup, name='signup'),
    path('employee/profile/', my_profile, name='my_profile'),
    path('employee/profile/<int:emp_id>/', employee_profile, name='employee_profile'),
    path('user-management/', admin_user_management, name='admin_user_management'),
]
