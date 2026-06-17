from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance, LeaveRequest
from Employee.models import Employee
from django.contrib import messages
from Notifications.utils import send_notification

@login_required
def leave_dashboard(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "You do not have an Employee profile assigned to your account.")
        return redirect('home')

    today = timezone.localdate()
    # Check if clocked in today
    today_attendance = Attendance.objects.filter(employee=employee, date=today).first()
    
    # Handle Clock-in / Clock-out POST
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'clock_in':
            if not today_attendance:
                Attendance.objects.create(
                    employee=employee,
                    date=today,
                    clock_in=timezone.localtime().time()
                )
                messages.success(request, "Clocked in successfully!")
            else:
                messages.warning(request, "You have already clocked in today.")
        elif action == 'clock_out':
            if today_attendance:
                if not today_attendance.clock_out:
                    today_attendance.clock_out = timezone.localtime().time()
                    today_attendance.save()
                    messages.success(request, "Clocked out successfully!")
                else:
                    messages.warning(request, "You have already clocked out today.")
            else:
                messages.error(request, "You must clock in first before clocking out.")
        
        elif action == 'request_leave':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            leave_type = request.POST.get('leave_type')
            if start_date and end_date and leave_type:
                LeaveRequest.objects.create(
                    employee=employee,
                    start_date=start_date,
                    end_date=end_date,
                    leave_type=leave_type,
                    status='Pending'
                )
                messages.success(request, "Leave request submitted successfully!")
            else:
                messages.error(request, "Please fill in all leave request fields.")
                
        return redirect('leave_dashboard')

    attendance_history = Attendance.objects.filter(employee=employee).order_by('-date')[:10]
    leave_requests = LeaveRequest.objects.filter(employee=employee).order_by('-start_date')

    # If manager or admin, get pending leave requests for approval
    is_manager = employee.employee_role in ['Manager', 'Admin']
    pending_leaves = []
    if is_manager:
        # Get all pending leaves for approval
        pending_leaves = LeaveRequest.objects.filter(status='Pending').order_by('start_date')

    return render(request, 'leave/dashboard.html', {
        'employee': employee,
        'today_attendance': today_attendance,
        'attendance_history': attendance_history,
        'leave_requests': leave_requests,
        'pending_leaves': pending_leaves,
        'is_manager': is_manager,
    })

@login_required
def approve_leave(request, leave_id):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect('home')

    if employee.employee_role not in ['Manager', 'Admin']:
        messages.error(request, "Only managers and admins can approve leave requests.")
        return redirect('leave_dashboard')

    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    action = request.POST.get('action') # 'approve' or 'reject'
    if action == 'approve':
        leave_request.status = 'Approved'
        messages.success(request, f"Leave request for {leave_request.employee.employee_name} has been approved.")
        send_notification(
            recipient=leave_request.employee,
            title="Leave Approved ✅",
            message=f"Your {leave_request.leave_type} leave request from {leave_request.start_date} to {leave_request.end_date} has been approved by {employee.employee_name}.",
            category='leave',
        )
    elif action == 'reject':
        leave_request.status = 'Rejected'
        messages.success(request, f"Leave request for {leave_request.employee.employee_name} has been rejected.")
        send_notification(
            recipient=leave_request.employee,
            title="Leave Rejected ❌",
            message=f"Your {leave_request.leave_type} leave request from {leave_request.start_date} to {leave_request.end_date} has been rejected by {employee.employee_name}.",
            category='leave',
        )
    leave_request.save()
    return redirect('leave_dashboard')

