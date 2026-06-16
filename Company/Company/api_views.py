from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from Employee.models import Employee
from Departments.models import Department
from Leave.models import Attendance, LeaveRequest
from Projects.models import Project, Task
from Payroll.models import SalaryDetails, Payslip
from Documents.models import Document

from Employee.serializers import EmployeeSerializer
from Departments.serializers import DepartmentSerializer
from Leave.serializers import AttendanceSerializer, LeaveRequestSerializer
from Projects.serializers import ProjectSerializer, TaskSerializer
from Payroll.serializers import SalaryDetailsSerializer, PayslipSerializer
from Documents.serializers import DocumentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class SalaryDetailsViewSet(viewsets.ModelViewSet):
    queryset = SalaryDetails.objects.all()
    serializer_class = SalaryDetailsSerializer
    permission_classes = [IsAuthenticated]

class PayslipViewSet(viewsets.ModelViewSet):
    queryset = Payslip.objects.all()
    serializer_class = PayslipSerializer
    permission_classes = [IsAuthenticated]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
