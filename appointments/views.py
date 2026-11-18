from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import HospitalProfile, User
from donations.models import DonationRequest
from .forms import AppointmentForm
from .models import Appointment
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from core.utils import create_notification
from core.models import Notification

@login_required
def hospital_schedule_appointment(request, application_id):
    if request.user.role != User.Role.HOSPITAL:
        messages.error(request, "Access denied.")
        return redirect("hospital-login")
    try:
        hospital = request.user.hospital_profile
    except HospitalProfile.DoesNotExist:
        messages.error(request, "Hospital profile not found.")
        return redirect("hospital-login")

    if hospital.verification_status != HospitalProfile.VerificationStatus.VERIFIED:
        messages.error(request, "Hospital account not verified.")
        return redirect("hospital-login")

    application = get_object_or_404(
        DonationRequest.objects.filter(assigned_hospital=request.user),
        pk=application_id,
    )

    if request.method == "POST":
        form = AppointmentForm(request.POST, hospital=request.user)
    else:
        form = AppointmentForm(
            hospital=request.user,
            initial={"donation_request": application},
        )

    # The application is selected by the URL, not by user input.
    form.fields.pop("donation_request")

    if request.method == "POST":
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.donation_request = application
            appointment.donor = application.donor
            appointment.hospital = request.user
            appointment.status = Appointment.Status.SCHEDULED
            appointment.save()

            # Create a donor in-app notification
            create_notification(
                recipient=appointment.donor,
                notification_type=Notification.NotificationType.APPOINTMENT_SCHEDULED,
                title="Appointment Scheduled",
                message=(
                    f"Your appointment has been scheduled for "
                    f"{appointment.appointment_date:%d %B %Y} at "
                    f"{appointment.appointment_time:%I:%M %p}. "
                    f"Location: {appointment.location or 'To be communicated'}."
                ),
            )

            messages.success(request, "Appointment scheduled successfully.")
            return redirect("hospital-appointment-list")

    return render(
        request,
        "hospital/appointments/schedule.html",
        {
            "form": form,
            "application": application,
        },
    )


@login_required
def hospital_appointment_list(request):
    if request.user.role != User.Role.HOSPITAL:
        messages.error(request, "Access denied.")
        return redirect("hospital-login")
    try:
        hospital = request.user.hospital_profile
    except HospitalProfile.DoesNotExist:
        messages.error(request, "Hospital profile not found.")
        return redirect("hospital-login")

    if hospital.verification_status != HospitalProfile.VerificationStatus.VERIFIED:
        messages.error(request, "Hospital account not verified.")
        return redirect("hospital-login")

    appointments = (
        Appointment.objects.filter(hospital=request.user)
        .select_related("donor", "donation_request")
        .order_by("-appointment_date", "-appointment_time")
    )

    search_query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "").strip()

    if search_query:
        appointments = appointments.filter(
            Q(donor__username__icontains=search_query)
            | Q(donor__first_name__icontains=search_query)
            | Q(donor__last_name__icontains=search_query)
            | Q(donor__email__icontains=search_query)
            | Q(donation_request__id__icontains=search_query)
            | Q(id__icontains=search_query)
        )

    valid_statuses = [choice[0] for choice in Appointment.Status.choices]

    if selected_status in valid_statuses:
        appointments = appointments.filter(status=selected_status)
    else:
        selected_status = ""

    paginator = Paginator(appointments, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "appointments": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "selected_status": selected_status,
        "status_choices": Appointment.Status.choices,
        "total_appointments": Appointment.objects.filter(
            hospital=request.user
        ).count(),
    }

    return render(request, "hospital/appointments/list.html", context,)


@login_required
@require_POST
def hospital_complete_appointment(request, appointment_id):
    if request.user.role != User.Role.HOSPITAL:
        messages.error(request, "Access denied.")
        return redirect("hospital-login")

    try:
        hospital = request.user.hospital_profile
    except HospitalProfile.DoesNotExist:
        messages.error(request, "Hospital profile not found.")
        return redirect("hospital-login")

    if hospital.verification_status != HospitalProfile.VerificationStatus.VERIFIED:
        messages.error(request, "Hospital account not verified.")
        return redirect("hospital-login")

    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
        hospital=request.user,
        status=Appointment.Status.SCHEDULED,
    )

    appointment.status = Appointment.Status.COMPLETED
    appointment.save(update_fields=["status", "updated_at"])

    messages.success(request, "Appointment marked as completed.")
    return redirect("hospital-appointment-list")


@login_required
@require_POST
def hospital_cancel_appointment(request, appointment_id):
    if request.user.role != User.Role.HOSPITAL:
        messages.error(request, "Access denied.")
        return redirect("hospital-login")
    try:
        hospital = request.user.hospital_profile
    except HospitalProfile.DoesNotExist:
        messages.error(request, "Hospital profile not found.")
        return redirect("hospital-login")

    if hospital.verification_status != HospitalProfile.VerificationStatus.VERIFIED:
        messages.error(request, "Hospital account not verified.")
        return redirect("hospital-login")

    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
        hospital=request.user,
        status=Appointment.Status.SCHEDULED,
    )

    appointment.status = Appointment.Status.CANCELLED
    appointment.save(update_fields=["status", "updated_at"])

    messages.success(request, "Appointment successfully cancelled.")
    return redirect("hospital-appointment-list")



