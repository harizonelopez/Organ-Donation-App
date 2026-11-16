from django.conf import settings
from django.db import models

class MedicalRecord(models.Model):
    class DocumentType(models.TextChoices):
        MEDICAL_REPORT = "MEDICAL_REPORT", "Medical Report"
        BLOOD_TEST = "BLOOD_TEST", "Blood Test"
        MEDICAL_HISTORY = "MEDICAL_HISTORY", "Medical History"
        OTHER = "OTHER", "Other"

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending Review"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_records",
        limit_choices_to={"role": "DONOR"},
    )

    donation_request = models.ForeignKey(
        "donations.DonationRequest",
        on_delete=models.CASCADE,
        related_name="medical_records",
    )

    document = models.FileField(
        upload_to="medical_records/%Y/%m/",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.donor.username}"

    class Meta:
        ordering = ["-uploaded_at"]
