from django.db import models
from Employee.models import Employee
from Departments.models import Department

class Project(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    deadline = models.DateField()
    status = models.CharField(max_length=50, default='In Progress')

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='To Do')
