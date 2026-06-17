from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee
from Departments.models import Department
from .forms import EmployeeSignupForm


# Create your views here.

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


@login_required
def add_employee(request):
    """View to add a new employee"""
    if request.method == "POST":
        employee_name = request.POST['emp_name']
        employee_age = request.POST['emp_age']
        employee_address = request.POST['emp_address']
        employee_department = request.POST['emp_department']
        employee_reporting_manager = request.POST['emp_reporting_manager']
        employee_email = request.POST['emp_email']
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


@login_required
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


@login_required
def delete_employee(request, emp_id):
    """view to delete an employee"""
    employee = Employee.objects.get(id=emp_id)
    employee.delete()
    return render(request, 'message.html', context={
        'msg': 'employee data deleted successfully'})


@login_required
def employee_detail(request, emp_id):
    """ View to see details of a specific employee"""
    employee = Employee.objects.get(id=emp_id)
    return render(request, 'employee/view.html', {'employee': employee})


@login_required
def employee_list(request):
    """ View to list all employees"""
    employees = Employee.objects.all()
    return render(request, 'employee/view_id.html', context={'employees': employees})


def signup(request):
    """Signup must remain public so new users can register"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            with transaction.atomic():
                user = User.objects.create_user(username=username, password=password)
                employee = form.save(commit=False)
                employee.user = user
                employee.employee_role = 'Employee'
                employee.save()

            login(request, user)
            return redirect('home')
    else:
        form = EmployeeSignupForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def my_profile(request):
    """View and edit own employee profile."""
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "You don't have an employee profile yet.")
        return redirect('home')

    if request.method == 'POST':
        employee.bio = request.POST.get('bio', employee.bio)
        employee.phone = request.POST.get('phone', employee.phone)
        employee.contract_type = request.POST.get('contract_type', employee.contract_type)
        employee.employee_address = request.POST.get('employee_address', employee.employee_address)

        if request.FILES.get('photo'):
            employee.photo = request.FILES['photo']

        employee.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('my_profile')

    return render(request, 'employee/profile.html', {
        'profile_employee': employee,
        'is_own_profile': True,
        'can_edit': True,
        'contract_choices': Employee.CONTRACT_CHOICES,
        'role_choices': Employee.ROLE_CHOICES,
    })


@login_required
def employee_profile(request, emp_id):
    """View any employee's profile. Admins/Managers can edit any profile."""
    profile_employee = get_object_or_404(Employee, id=emp_id)

    try:
        viewer = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect('home')

    is_own_profile = (viewer.id == profile_employee.id)
    can_edit = is_own_profile or viewer.employee_role in ['Admin', 'Manager']

    if request.method == 'POST' and can_edit:
        profile_employee.bio = request.POST.get('bio', profile_employee.bio)
        profile_employee.phone = request.POST.get('phone', profile_employee.phone)
        profile_employee.contract_type = request.POST.get('contract_type', profile_employee.contract_type)
        profile_employee.employee_address = request.POST.get('employee_address', profile_employee.employee_address)

        if viewer.employee_role in ['Admin', 'Manager']:
            profile_employee.employee_name = request.POST.get('employee_name', profile_employee.employee_name)
            profile_employee.employee_department = request.POST.get('employee_department', profile_employee.employee_department)
            profile_employee.employee_role = request.POST.get('employee_role', profile_employee.employee_role)

        if request.FILES.get('photo'):
            profile_employee.photo = request.FILES['photo']

        profile_employee.save()
        messages.success(request, f"Profile updated for {profile_employee.employee_name}!")
        return redirect('employee_profile', emp_id=emp_id)

    return render(request, 'employee/profile.html', {
        'profile_employee': profile_employee,
        'is_own_profile': is_own_profile,
        'can_edit': can_edit,
        'contract_choices': Employee.CONTRACT_CHOICES,
        'role_choices': Employee.ROLE_CHOICES,
    })