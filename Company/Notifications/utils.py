from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def send_notification(recipient, title, message, category='system'):
    """
    Create an in-app notification for a given employee and send an email notification.

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

    if recipient.employee_email:
        try:
            subject = f"[CorpNexus] {title}"
            body = (
                f"Hello {recipient.employee_name},\n\n"
                f"{message}\n\n"
                f"Regards,\n"
                f"CorpNexus Team"
            )
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.employee_email],
                fail_silently=True
            )
        except Exception as e:
            # Fail silently to prevent user action from breaking if mail service is down
            pass

