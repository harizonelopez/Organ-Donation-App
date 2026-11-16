from django.contrib import admin
from .models import Notification, ActivityLog

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "title",
        "is_read",
        "created_at",
    )

    list_filter = ("is_read", "created_at")

    search_fields = (
        "recipient__username",
        "title",
        "message",
    )

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "ip_address",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user__username",
        "action",
        "description",
    )

    readonly_fields = (
        "user",
        "action",
        "description",
        "ip_address",
        "created_at",
    )

