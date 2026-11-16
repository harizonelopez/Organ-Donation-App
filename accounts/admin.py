from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import User, DonorProfile, HospitalProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Application Role", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Application Role", {"fields": ("role",)}),
    )

    list_display = (
        "username",
        "email",
        "role",
        "is_active",
        "is_staff",
    )

    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "city",
        "country",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone_number",
    )

    list_filter = ("country", "city")
    list_select_related = ("user",)


@admin.register(HospitalProfile)
class HospitalProfileAdmin(admin.ModelAdmin):
    list_display = (
        "hospital_name",
        "registration_number",
        "user",
        "verification_status",
        "city",
        "country",
    )

    list_filter = (
        "verification_status",
        "country",
    )

    search_fields = (
        "hospital_name",
        "registration_number",
        "user__username",
        "user__email",
    )

    list_select_related = ("user",)

    readonly_fields = (
        "user",
        "created_at",
        "updated_at",
    )

    actions = (
        "verify_hospitals",
        "reject_hospitals",
    )

    @admin.action(description="Verify selected hospital accounts")
    def verify_hospitals(self, request, queryset):
        updated = queryset.update(
            verification_status=HospitalProfile.VerificationStatus.VERIFIED
        )

        self.message_user(
            request,
            f"{updated} hospital account(s) successfully verified.",
            messages.SUCCESS,
        )

    @admin.action(description="Reject selected hospital accounts")
    def reject_hospitals(self, request, queryset):
        updated = queryset.update(
            verification_status=HospitalProfile.VerificationStatus.REJECTED
        )

        self.message_user(
            request,
            f"{updated} hospital account(s) rejected.",
            messages.WARNING,
        )



