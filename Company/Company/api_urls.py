from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    EmployeeViewSet, DepartmentViewSet, AttendanceViewSet,
    LeaveRequestViewSet, ProjectViewSet, TaskViewSet,
    SalaryDetailsViewSet, PayslipViewSet, DocumentViewSet
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'salary-details', SalaryDetailsViewSet)
router.register(r'payslips', PayslipViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
