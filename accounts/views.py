from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import DonorRegistrationForm, HospitalRegistrationForm
from .models import User, DonorProfile, HospitalProfile
from donations.models import DonationRequest
from medical_records.models import MedicalRecord
from appointments.models import Appointment
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from donations.models import DonationReview
from core.models import Notification


def welcome(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.DONOR:
            return redirect("donor-dashboard")

        if request.user.role == User.Role.HOSPITAL:
            try:
                profile = request.user.hospital_profile
                if profile.verification_status == HospitalProfile.VerificationStatus.VERIFIED:
                    return redirect("hospital-dashboard")

                logout(request)
            except HospitalProfile.DoesNotExist:
                logout(request)

    return render(request, "accounts/welcome.html")


def donor_register(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.DONOR:
            return redirect("donor-dashboard")
        return redirect("admin:index")

    if request.method == "POST":
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.role = User.Role.DONOR
                user.save()

                DonorProfile.objects.create(
                    user=user,
                    phone_number=form.cleaned_data["phone_number"],
                    date_of_birth=form.cleaned_data["date_of_birth"],
                    address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"],
                    country=form.cleaned_data["country"],
                )

            login(request, user)

            messages.success(request, "Donor account successfully created.")
            return redirect("donor-dashboard")

    else:
        form = DonorRegistrationForm()
    return render(request, "accounts/donor_register.html", {"form": form})


def hospital_register(request):
    # An authenticated administrator or donor can still access this page.
    if request.method == "POST":
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.role = User.Role.HOSPITAL
                user.is_staff = False
                user.is_superuser = False
                user.save()

                HospitalProfile.objects.create(
                    user=user,
                    hospital_name=form.cleaned_data["hospital_name"],
                    registration_number=form.cleaned_data["registration_number"],
                    contact_number=form.cleaned_data["contact_number"],
                    address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"],
                    country=form.cleaned_data["country"],
                )

            messages.success(
                request,
                "Hospital registration submitted successfully. "
                "Account awaiting administrator verification."
            )
            return redirect("hospital-login")
    else:
        form = HospitalRegistrationForm()

    return render(request, "accounts/hospital_register.html",  {"form": form})


def hospital_login(request):
    if request.user.is_authenticated and request.user.role == User.Role.HOSPITAL:
        try:
            profile = request.user.hospital_profile
            if profile.verification_status == HospitalProfile.VerificationStatus.VERIFIED:
                return redirect("hospital-dashboard")

            logout(request)
            if profile.verification_status == HospitalProfile.VerificationStatus.PENDING:
                messages.warning(request, "Hospital account awaiting administrator verification.")
            else:
                messages.error(request, "Hospital registration rejected. Contact administrator.")

        except HospitalProfile.DoesNotExist:
            logout(request)
            messages.error(request, "Hospital profile not found.")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role != User.Role.HOSPITAL:
                messages.error(request, "Credentials doesn't belong to a hospital account.")
            else:
                try:
                    profile = user.hospital_profile
                    if profile.verification_status == HospitalProfile.VerificationStatus.VERIFIED:
                        login(request, user)
                        return redirect("hospital-dashboard")
                    elif profile.verification_status == HospitalProfile.VerificationStatus.PENDING:
                        messages.warning(request, "Hospital account awaiting administrator verification.")
                    else:
                        messages.error(request, "Hospital registration rejected. Contact administrator.")
                except HospitalProfile.DoesNotExist:
                    messages.error(request, "Hospital profile not found.")
        else:
            messages.error(request, "Invalid hospital username or password.")
    else:
        form = AuthenticationForm(request)

    # Style login fields
    for field_name, field in form.fields.items():
        field.widget.attrs.update({
            "class": "form-control",
            "placeholder": (
                "Enter hospital username"
                if field_name == "username"
                else "Enter password"
            ),
            "autocomplete": (
                "username"
                if field_name == "username"
                else "current-password"
            ),
        })
    return render(request, "accounts/hospital_login.html", {"form": form})


def donor_login(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.DONOR:
            return redirect("donor-dashboard")

        messages.error(request, "You are already signed in with another account.")
        return redirect("admin:index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user.role != User.Role.DONOR:
                messages.error(request, "Login page is for donor accounts only.")
            else:
                login(request, user)
                return redirect("donor-dashboard")

    else:
        form = AuthenticationForm(request)
    return render(request, "accounts/donor_login.html", {"form": form})


@login_required
def donor_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("donor-login")

    return redirect("donor-dashboard")


@login_required
def donor_dashboard(request):
    if request.user.role != User.Role.DONOR:
        messages.error(request, "Access denied..")
        return redirect("donor-login")

    applications = DonationRequest.objects.filter(
        donor=request.user
    ).order_by("-submitted_at")

    medical_records = MedicalRecord.objects.filter(
        donor=request.user
    )

    appointments = Appointment.objects.filter(
        donor=request.user,
        status="SCHEDULED"
    ).order_by("appointment_date", "appointment_time")

    recent_notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")[:3]

    context = {
        "total_applications": applications.count(),

        "pending_applications": applications.filter(
            status__in=["SUBMITTED", "UNDER_REVIEW"]
        ).count(),

        "approved_applications": applications.filter(
            status="APPROVED"
        ).count(),

        "total_medical_records": medical_records.count(),

        "recent_applications": applications[:5],

        "upcoming_appointments": appointments,

        "recent_notifications": recent_notifications,

        "unread_notifications": Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count(),
    }
    return render(request, "donor/dashboard.html", context)


@login_required
def hospital_dashboard(request):
    if request.user.role != User.Role.HOSPITAL:
        messages.error(request, "Access denied.")
        return redirect("hospital-login")

    try:
        profile = request.user.hospital_profile
    except HospitalProfile.DoesNotExist:
        messages.error(request, "Hospital profile not found.")
        logout(request)
        return redirect("hospital-login")

    if profile.verification_status != HospitalProfile.VerificationStatus.VERIFIED:
        logout(request)
        messages.warning(request, "Hospital account awaiting Administrator verification.")
        return redirect("hospital-login")

    # Applications assigned specifically to the hospital
    assigned_applications = DonationRequest.objects.filter(
        assigned_hospital=request.user
    )

    # Hospital-specific review records
    reviews = DonationReview.objects.filter(hospital=request.user)

    total_assigned_applications = assigned_applications.count()
    unreviewed_applications = assigned_applications.filter(
        status="SUBMITTED"
    ).count()

    applications_under_review = assigned_applications.filter(
        status="UNDER_REVIEW"
    ).count()

    total_cases_reviewed = (
        reviews.values("donation_request_id").distinct().count()
    )

    pending_reviews = (
        reviews.filter(decision="UNDER_REVIEW")
        .values("donation_request_id")
        .distinct()
        .count()
    )

    approved_reviews = (
        reviews.filter(decision="APPROVED")
        .values("donation_request_id")
        .distinct()
        .count()
    )

    rejected_reviews = (
        reviews.filter(decision="REJECTED")
        .values("donation_request_id")
        .distinct()
        .count()
    )

    # Hospital-specific appointments
    hospital_appointments = Appointment.objects.filter(
        hospital=request.user
    )

    today = timezone.localdate()

    upcoming_appointments = hospital_appointments.filter(
        appointment_date__gte=today
    ).exclude(
        status__in=["CANCELLED", "COMPLETED"]
    )

    completed_appointments = hospital_appointments.filter(
        status="COMPLETED"
    ).count()

    # Monthly review activity over approximately 6 months
    six_months_ago = timezone.now() - timedelta(days=180)

    monthly_reviews = (
        reviews.filter(reviewed_at__gte=six_months_ago)
        .annotate(month=TruncMonth("reviewed_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    review_trend_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_reviews
    ]

    review_trend_values = [
        item["total"]
        for item in monthly_reviews
    ]

    # Review decision distribution
    review_status_labels = ["Under review", "Approved", "Rejected"]
    review_status_values = [
        pending_reviews,
        approved_reviews,
        rejected_reviews,
    ]

    # Appointment status distribution
    appointment_statuses = (
        hospital_appointments.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    appointment_choices = dict(
        Appointment._meta.get_field("status").choices
    )

    appointment_chart_labels = [
        appointment_choices.get(item["status"], item["status"])
        for item in appointment_statuses
    ]

    appointment_chart_values = [
        item["total"] for item in appointment_statuses
    ]

    # Recent hospital reviews
    recent_reviews = (
        reviews.select_related(
            "donation_request",
            "donation_request__donor",
        )
        .order_by("-reviewed_at")[:6]
    )

    # Upcoming appointments
    upcoming_appointments_list = (
        upcoming_appointments.select_related(
            "donor",
            "donation_request",
        )
        .order_by("appointment_date", "appointment_time")[:6]
    )

    context = {
        "hospital_profile": profile,

        "total_cases_reviewed": total_cases_reviewed,
        "pending_reviews": pending_reviews,
        "approved_reviews": approved_reviews,
        "rejected_reviews": rejected_reviews,

        "upcoming_appointments_count": upcoming_appointments.count(),
        "completed_appointments": completed_appointments,

        "review_trend_labels": review_trend_labels,
        "review_trend_values": review_trend_values,

        "review_status_labels": review_status_labels,
        "review_status_values": review_status_values,

        "appointment_chart_labels": appointment_chart_labels,
        "appointment_chart_values": appointment_chart_values,

        "recent_reviews": recent_reviews,
        "upcoming_appointments_list": upcoming_appointments_list,

        "total_assigned_applications": total_assigned_applications,
        "unreviewed_applications": unreviewed_applications,
        "applications_under_review": applications_under_review,
    }
    return render(request, "hospital/dashboard.html", context)


@login_required
@require_POST
def hospital_logout(request):
    if request.user.role != User.Role.HOSPITAL:
        messages.error(request, "Action available only for hospital accounts.")
        return redirect("hospital-login")
    
    logout(request)
    return redirect("hospital-login")


