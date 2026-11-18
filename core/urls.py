from django.urls import path
from . import views

urlpatterns = [
    path("notifications/", views.notification_list, name="notification-list"),
    path(
        "notifications/<int:notification_id>/read", 
        views.mark_notification_read,
        name="mark-notification-read",
    ),
]