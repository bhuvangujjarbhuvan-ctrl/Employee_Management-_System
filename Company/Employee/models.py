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
    CONTRACT_CHOICES = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Intern', 'Intern'),
    )
    employee_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    
    employee_name = models.CharField(max_length=50, default=None)
    employee_age = models.CharField(max_length=30, default=None)
    employee_address = models.CharField(max_length=100, default=None)
    employee_department = models.CharField(max_length=30, default=None)
    employee_reporting_manager = models.CharField(max_length=50, default=None)
    employee_email = models.CharField(max_length=50, unique=True)

    # Profile fields
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='Full-Time')
    date_joined = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.employee_name