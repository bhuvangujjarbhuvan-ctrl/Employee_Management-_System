from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from .models import Notification
from Employee.models import Employee


@login_required
def notifications_list(request):
    """Renders the full notifications page."""
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return redirect('home')

    notifications = Notification.objects.filter(recipient=employee)
    unread_count = notifications.filter(is_read=False).count()

    return TemplateResponse(request, 'notifications/list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
@require_POST
def mark_read(request, notif_id):
    """Mark a single notification as read."""
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'No employee profile'}, status=403)

    notif = get_object_or_404(Notification, id=notif_id, recipient=employee)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def mark_all_read(request):
    """Mark all notifications as read."""
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'No employee profile'}, status=403)

    Notification.objects.filter(recipient=employee, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
def unread_count_api(request):
    """JSON endpoint — returns unread notification count for the navbar badge."""
    try:
        employee = request.user.employee
        count = Notification.objects.filter(recipient=employee, is_read=False).count()
    except Employee.DoesNotExist:
        count = 0
    return JsonResponse({'count': count})
