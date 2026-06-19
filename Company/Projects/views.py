from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from Employee.models import Employee
from Departments.models import Department
from django.contrib import messages

@login_required
def projects_dashboard(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "You do not have an Employee profile assigned to your account.")
        return redirect('home')

    # Handle POST requests (creation / updates)
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_project' and employee.employee_role in ['Admin', 'Manager']:
            name = request.POST.get('name')
            dept_id = request.POST.get('department')
            deadline = request.POST.get('deadline')
            status = request.POST.get('status', 'In Progress')

            department = get_object_or_404(Department, id=dept_id)
            project = Project.objects.create(
                name=name,
                department=department,
                deadline=deadline,
                status=status
            )
            messages.success(request, f"Project '{project.name}' created successfully!")
            return redirect('projects_dashboard')

        elif action == 'create_task' and employee.employee_role in ['Admin', 'Manager']:
            project_id = request.POST.get('project')
            emp_id = request.POST.get('assigned_employee')
            title = request.POST.get('title')
            status = request.POST.get('status', 'To Do')

            project = get_object_or_404(Project, id=project_id)
            assigned_emp = get_object_or_404(Employee, id=emp_id)
            task = Task.objects.create(
                project=project,
                assigned_employee=assigned_emp,
                title=title,
                status=status
            )
            messages.success(request, f"Task '{task.title}' assigned to {assigned_emp.employee_name} successfully!")
            return redirect('projects_dashboard')

        else:
            # Default fallback for self-updating task status
            task_id = request.POST.get('task_id')
            new_status = request.POST.get('status')
            task = get_object_or_404(Task, id=task_id, assigned_employee=employee)
            if new_status in ['To Do', 'In Progress', 'Completed']:
                task.status = new_status
                task.save()
                messages.success(request, f"Task '{task.title}' updated to {new_status}!")
            return redirect('projects_dashboard')

    # My tasks
    my_tasks = Task.objects.filter(assigned_employee=employee).order_by('status')

    # All active projects
    all_projects = Project.objects.all().order_by('deadline')

    # Privileged data for project/task creator forms
    departments = []
    all_employees = []
    is_privileged = employee.employee_role in ['Admin', 'Manager']
    if is_privileged:
        departments = Department.objects.all()
        all_employees = Employee.objects.all().order_by('employee_name')

    return render(request, 'projects/dashboard.html', {
        'employee': employee,
        'my_tasks': my_tasks,
        'all_projects': all_projects,
        'departments': departments,
        'all_employees': all_employees,
        'is_privileged': is_privileged,
    })


