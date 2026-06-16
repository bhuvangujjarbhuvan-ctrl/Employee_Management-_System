from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from Employee.models import Employee
from django.contrib import messages

@login_required
def projects_dashboard(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "You do not have an Employee profile assigned to your account.")
        return redirect('home')

    # Handle Task status updates
    if request.method == 'POST':
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

    return render(request, 'projects/dashboard.html', {
        'employee': employee,
        'my_tasks': my_tasks,
        'all_projects': all_projects,
    })

