from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "donor",
        "hospital",
        "appointment_date",
        "appointment_time",
        "status",
    )

    list_filter = (
        "status",
        "appointment_date",
        "hospital",
    )

    search_fields = (
        "donor__username",
        "hospital__username",
    )

    readonly_fields = ("created_at", "updated_at")

