from django.conf import settings
from django.db import models

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SCHEDULED = "SCHEDULED", "Scheduled"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    donation_request = models.ForeignKey(
        "donations.DonationRequest",
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
        limit_choices_to={"role": "DONOR"},
    )

    hospital = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="hospital_appointments",
        limit_choices_to={"role": "HOSPITAL"},
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    hospital_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment #{self.pk} - {self.donor.username}"

    class Meta:
        ordering = ["appointment_date", "appointment_time"]
        
