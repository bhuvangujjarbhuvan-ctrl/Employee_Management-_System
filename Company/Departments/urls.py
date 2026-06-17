from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='Department Home'),
    path('department/add/', add_department, name='Add Department'),
    path('department/department_list/', department_list, name='Department List'),  # ✅ fixed
    path('department/delete/<int:dept_id>/', delete_department, name='Delete Department'),
    path('department/edit_department/<int:dept_id>/', edit_department, name='Edit Department'),
    path('department/department_detail/<int:dept_id>/', department_detail, name='Department Detail'),
    path('department/analytics/', department_analytics, name='Department Analytics'),
]
