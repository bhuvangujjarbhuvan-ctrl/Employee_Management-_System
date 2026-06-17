from django.db import models
from Employee.models import Employee


class Notification(models.Model):
    CATEGORY_CHOICES = (
        ('leave', 'Leave'),
        ('payroll', 'Payroll'),
        ('task', 'Task'),
        ('system', 'System'),
    )

    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=120)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.category}] {self.title} → {self.recipient.employee_name}"
