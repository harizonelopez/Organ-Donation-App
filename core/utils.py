from .models import Notification

def create_notification(recipient, notification_type, title, message):
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
    )

