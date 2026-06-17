"""
Notification utility helpers.
Use send_notification() anywhere in the project to create an in-app notification.
"""
from .models import Notification


def send_notification(recipient, title, message, category='system'):
    """
    Create an in-app notification for a given employee.

    Args:
        recipient (Employee): The Employee instance to notify.
        title (str): Short notification headline.
        message (str): Full notification body.
        category (str): One of 'leave', 'payroll', 'task', 'system'.
    """
    Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        category=category,
    )
