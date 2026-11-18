from .models import Notification

def unread_notification_count(request):
    if request.user.is_authenticated and request.user.role == "DONOR":
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count()

        return {"unread_notification_count": count}
    return {"unread_notification_count": 0}


