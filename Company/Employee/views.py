from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Employee
from Departments.models import Department
from .forms import EmployeeSignupForm


#Create your views here.

def home(request):
    """ Renders the home page or landing page depending on authentication status """
    if not request.user.is_authenticated:
        return render(request, 'landing.html')
        
    employee_count = Employee.objects.count()
    department_count = Department.objects.count()
    return render(request, 'home.html', {
        'employee_count': employee_count,
        'department_count': department_count,
    })

#Additional views for employee operations can be added here

def add_employee(request):
    """View to add a new employee"""
    if request.method == "POST":
        employee_name = request.POST['emp_name']
        employee_age = request.POST['emp_age']
        employee_address = request.POST['emp_address']
        employee_department = request.POST['emp_department']
        employee_reporting_manager = request.POST['emp_reporting_manager']
        employee_email = request.POST['emp_email']
        # creating a class in the object
        employee_data = Employee(
            employee_name=employee_name,
            employee_age=employee_age,
            employee_address=employee_address,
            employee_department=employee_department,
            employee_reporting_manager=employee_reporting_manager,
            employee_email=employee_email
        )
        employee_data.save()
        return render(request, 'message.html', context={
            'msg': 'Employee registered successfully!'
        })
    departments = Department.objects.all()
    return render(request, 'employee/add.html', {'departments': departments})

def edit_employee(request, emp_id):
    """ View to edit an existing employee"""
    employee = Employee.objects.get(id=emp_id)
    if request.method == "POST":
        employee.employee_name = request.POST['emp_name']
        employee.employee_age = request.POST['emp_age']
        employee.employee_address = request.POST['emp_address']
        employee.employee_department = request.POST['emp_department']
        employee.employee_reporting_manager = request.POST['emp_reporting_manager']
        employee.employee_email = request.POST['emp_email']
        employee.save()
        return render(request, 'message.html', context={'msg': 'Employee data updated successfully!'})
    departments = Department.objects.all()
    return render(request, 'employee/edit.html', context={'employee': employee, 'departments': departments})

def delete_employee(request, emp_id): 
    """view to delete an employee"""
    employee = Employee.objects.get(id = emp_id)
    employee.delete()
    return render(request, 'message.html', context={
        'msg':'employee data deleted successfully'})

def employee_detail(request, emp_id):
    """ View to see details of a specific employee"""
    employee= Employee.objects.get(id=emp_id)
    return render(request, 'employee/view.html', {'employee': employee})

def employee_list(request):
    """ View to list all employees"""
    employees = Employee.objects.all()
    return render(request, 'employee/view_id.html', context={'employees': employees})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(username=username, password=password)
                
                # Create associated employee profile
                employee = form.save(commit=False)
                employee.user = user
                employee.employee_role = 'Employee'  # Default role for new signups
                employee.save()
                
            # Log the user in directly after signup
            login(request, user)
            return redirect('home')
    else:
        form = EmployeeSignupForm()
        
    return render(request, 'registration/signup.html', {'form': form})