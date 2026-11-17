from django.conf import settings
from django.db import models

class DonationRequest(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="donation_requests",
        limit_choices_to={"role": "DONOR"},
    )

    assigned_hospital = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_donation_requests",
        limit_choices_to={"role": "HOSPITAL"},
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application #{self.pk} - {self.donor.username}"


class DonationOrgan(models.Model):
    class Organ(models.TextChoices):
        KIDNEY = "KIDNEY", "Kidney"
        LIVER = "LIVER", "Liver"
        HEART = "HEART", "Heart"
        LUNG = "LUNG", "Lung"
        PANCREAS = "PANCREAS", "Pancreas"
        CORNEA = "CORNEA", "Cornea"
        BONE_MARROW = "BONE_MARROW", "Bone Marrow"

    donation_request = models.ForeignKey(
        DonationRequest,
        on_delete=models.CASCADE,
        related_name="organs",
    )
    organ = models.CharField(
        max_length=20,
        choices=Organ.choices,
    )

    def __str__(self):
        return f"{self.get_organ_display()} - Application #{self.donation_request_id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["donation_request", "organ"],
                name="unique_organ_per_donation_request",
            )
        ]


class DonationReview(models.Model):
    class Decision(models.TextChoices):
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved for Further Evaluation"
        REJECTED = "REJECTED", "Rejected"

    donation_request = models.ForeignKey(
        DonationRequest,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    hospital = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="donation_reviews",
        limit_choices_to={"role": "HOSPITAL"},
    )
    decision = models.CharField(
        max_length=20,
        choices=Decision.choices,
    )
    comments = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review - Application #{self.donation_request_id}"

    class Meta:
        ordering = ["-reviewed_at"]

class HospitalApplicationNote(models.Model):
    donation_request = models.ForeignKey(
        DonationRequest,
        on_delete=models.CASCADE,
        related_name="hospital_notes",
    )
    hospital = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="application_notes",
        limit_choices_to={"role": "HOSPITAL"},
    )
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Hospital Note - Application #{self.donation_request_id}"
