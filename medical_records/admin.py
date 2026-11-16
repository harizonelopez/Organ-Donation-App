from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "donor",
        "donation_request",
        "document_type",
        "verification_status",
        "uploaded_at",
    )

    list_filter = (
        "document_type",
        "verification_status",
        "uploaded_at",
    )

    search_fields = (
        "donor__username",
        "donor__email",
    )

    readonly_fields = ("uploaded_at", "updated_at")

