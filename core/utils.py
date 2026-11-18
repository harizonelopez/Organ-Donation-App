import logging
from django.conf import settings
from django.core.mail import send_mail
from .models import Notification

logger = logging.getLogger(__name__)

def create_notification(recipient, notification_type, title, message):
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
    )

    if recipient.email and settings.DEFAULT_FROM_EMAIL:
        try:
            send_mail(
                subject=title,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                "Failed to send notification email to %s",
                recipient.email,
            )
    return notification

