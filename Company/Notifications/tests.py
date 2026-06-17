from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from Employee.models import Employee
from .models import Notification
from .utils import send_notification

class NotificationsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="notify_user", password="password123")
        self.employee = Employee.objects.create(
            user=self.user,
            employee_role="Employee",
            employee_name="Notify Employee",
            employee_age="28",
            employee_address="789 Lane",
            employee_department="Sales",
            employee_reporting_manager="Manager User",
            employee_email="notify_emp@company.com"
        )

    def test_send_notification_creates_db_entry_and_sends_email(self):
        """send_notification helper should write to database and send an email"""
        # Clear outbox
        mail.outbox = []
        
        send_notification(
            recipient=self.employee,
            title="Leave Request Approved",
            message="Your leave request from June 20 to June 22 has been approved.",
            category="leave"
        )
        
        # Verify DB entry
        notif = Notification.objects.filter(recipient=self.employee).first()
        self.assertIsNotNone(notif)
        self.assertEqual(notif.title, "Leave Request Approved")
        self.assertEqual(notif.category, "leave")
        self.assertFalse(notif.is_read)
        
        # Verify Email
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "[CorpNexus] Leave Request Approved")
        self.assertEqual(email.to, ["notify_emp@company.com"])
        self.assertIn("Hello Notify Employee", email.body)
        self.assertIn("Your leave request from June 20 to June 22 has been approved.", email.body)

    def test_unread_count_api(self):
        """Unread count API returns correct JSON value"""
        self.client.login(username="notify_user", password="password123")
        
        # Initially 0
        response = self.client.get(reverse('notification_unread_count'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
        
        # Add notifications
        send_notification(self.employee, "Alert 1", "Msg 1")
        send_notification(self.employee, "Alert 2", "Msg 2")
        
        response = self.client.get(reverse('notification_unread_count'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_mark_read_view(self):
        """Marking a notification as read updates its status"""
        send_notification(self.employee, "Alert 1", "Msg 1")
        notif = Notification.objects.filter(recipient=self.employee).first()
        self.assertFalse(notif.is_read)
        
        self.client.login(username="notify_user", password="password123")
        response = self.client.post(reverse('notification_mark_read', args=[notif.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
        
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
