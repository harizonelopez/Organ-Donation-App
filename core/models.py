from django.conf import settings
from django.db import models

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        APPOINTMENT_SCHEDULED = "APPOINTMENT_SCHEDULED", "Appointment Scheduled"
        APPOINTMENT_REMINDER = "APPOINTMENT_REMINDER", "Appointment Reminder"
        APPOINTMENT_RESCHEDULED = "APPOINTMENT_RESCHEDULED", "Appointment Rescheduled"
        APPOINTMENT_CANCELLED = "APPOINTMENT_CANCELLED", "Appointment Cancelled"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    notification_type = models.CharField(
        max_length=40,
        choices=NotificationType.choices,
        default=NotificationType.APPOINTMENT_SCHEDULED,
    )

    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"

class ActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
    )

    action = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.action
    
