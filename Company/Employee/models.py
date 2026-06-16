from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    )
    employee_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    
    employee_name=models.CharField(max_length=50,default=None)
    employee_age=models.CharField(max_length=30,default=None)
    employee_address=models.CharField(max_length=100,default=None)
    employee_department=models.CharField(max_length=30,default=None)
    employee_reporting_manager=models.CharField(max_length=50,default=None)
    employee_email=models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.employee_name