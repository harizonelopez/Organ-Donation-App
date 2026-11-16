from django import forms
from django.contrib import admin
from accounts.models import User, HospitalProfile
from .models import DonationRequest, DonationOrgan, DonationReview

class DonationOrganInline(admin.TabularInline):
    model = DonationOrgan
    extra = 1

class DonationRequestAdminForm(forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_hospital"].queryset = (
            User.objects.filter(
                role=User.Role.HOSPITAL,
                hospital_profile__verification_status=(
                    HospitalProfile.VerificationStatus.VERIFIED
                ),
            )
            .select_related("hospital_profile")
            .order_by("hospital_profile__hospital_name")
        )

@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    form = DonationRequestAdminForm
    list_display = (
        "id",
        "donor",
        "status",
        "assigned_hospital_name",
        "assignment_status",
        "submitted_at",
    )

    list_filter = (
        "status",
        "assigned_hospital",
        "submitted_at",
    )

    search_fields = (
        "donor__username",
        "donor__email",
        "assigned_hospital__username",
        "assigned_hospital__hospital_profile__hospital_name",
    )

    inlines = [DonationOrganInline]

    @admin.display(description="Assigned hospital")
    def assigned_hospital_name(self, obj):
        if obj.assigned_hospital:
            return obj.assigned_hospital.hospital_profile.hospital_name
        return "Not assigned"

    @admin.display(description="Assignment", boolean=True)
    def assignment_status(self, obj):
        return obj.assigned_hospital is not None

@admin.register(DonationReview)
class DonationReviewAdmin(admin.ModelAdmin):
    list_display = (
        "donation_request",
        "hospital",
        "decision",
        "reviewed_at",
    )

    list_filter = (
        "decision",
        "reviewed_at",
    )

    search_fields = (
        "donation_request__donor__username",
        "hospital__username",
        "hospital__hospital_profile__hospital_name",
    )

    readonly_fields = (
        "donation_request",
        "hospital",
        "decision",
        "comments",
        "reviewed_at",
    )

