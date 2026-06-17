from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department

# 🏠 Home Page
def home(request):
    """Renders the home page for Department app"""
    return render(request, 'home.html')


# 📋 List All Departments
@login_required
def department_list(request):
    """Returns all the Departments with their details"""
    departments = Department.objects.all()
    return render(request, 'department/department_list.html', {'departments': departments})


# ➕ Add a New Department
@login_required
def add_department(request):
    """Provides the form to add a new Department"""
    if request.method == 'POST':
        department_name = request.POST.get('dept_name')
        department_no_of_projects = request.POST.get('dept_projects')
        department_head = request.POST.get('dept_head')
        department_region = request.POST.get('dept_region')

        Department.objects.create(
            department_name=department_name,
            department_no_of_projects=department_no_of_projects,
            department_head=department_head,
            department_region=department_region
        )
        return render(request, 'deptmessage.html', {'msg': 'Department added successfully!'})

    return render(request, 'department/add_department.html')


# ✏️ Edit Department
@login_required
def edit_department(request, dept_id):
    """Provides the form to edit a Department"""
    department = get_object_or_404(Department, id=dept_id)

    if request.method == 'POST':
        department.department_name = request.POST.get('department_name')
        department.department_no_of_projects = request.POST.get('department_no_of_projects')
        department.department_head = request.POST.get('department_head')
        department.department_region = request.POST.get('department_region')
        department.save()
        return render(request, 'deptmessage.html', {'msg': 'Department updated successfully!', 'department': department})

    return render(request, 'department/edit_department.html', {'department': department})


# ❌ Delete Department
@login_required
def delete_department(request, dept_id):
    """Deletes a specific Department"""
    department = Department.objects.get(id=dept_id)
    department.delete()
    return render(request, 'deptmessage.html', {'msg': 'Department deleted successfully!'})


# 🔍 Department Detail
@login_required
def department_detail(request, dept_id):
    """Displays the details of a specific Department"""
    department = Department.objects.get(id=dept_id)
    return render(request, 'department/department_detail.html', {'department': department})


# 📊 Department Analytics
@login_required
def department_analytics(request):
    """Renders visual analytics and breakdown statistics for departments"""
    from Employee.models import Employee
    from Projects.models import Project, Task
    from Leave.models import LeaveRequest

    departments = Department.objects.all()
    dept_data = []

    for dept in departments:
        headcount = Employee.objects.filter(employee_department__iexact=dept.department_name).count()
        projects_count = Project.objects.filter(department=dept).count()
        
        # Tasks related to projects in this department
        dept_projects = Project.objects.filter(department=dept)
        tasks_todo = Task.objects.filter(project__in=dept_projects, status__iexact='To Do').count()
        tasks_progress = Task.objects.filter(project__in=dept_projects, status__iexact='In Progress').count()
        tasks_completed = Task.objects.filter(project__in=dept_projects, status__iexact='Completed').count()
        tasks_count = tasks_todo + tasks_progress + tasks_completed

        leaves_count = LeaveRequest.objects.filter(
            employee__employee_department__iexact=dept.department_name,
            status='Approved'
        ).count()

        dept_data.append({
            'name': dept.department_name,
            'headcount': headcount,
            'projects': projects_count,
            'tasks': tasks_count,
            'tasks_todo': tasks_todo,
            'tasks_progress': tasks_progress,
            'tasks_completed': tasks_completed,
            'leaves': leaves_count,
            'region': dept.department_region,
            'head': dept.department_head,
        })

    return render(request, 'department/analytics.html', {'dept_data': dept_data})

