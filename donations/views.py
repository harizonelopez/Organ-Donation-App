from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, HospitalProfile
from .forms import DonationApplicationForm
from .models import (DonationRequest, DonationOrgan, DonationReview, HospitalApplicationNote,)
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def donation_application(request):
    if request.user.role != User.Role.DONOR:
        messages.error(request, "Only donors can submit donation applications.")
        return redirect("donor-dashboard")

    if request.method == "POST":
        form = DonationApplicationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                application = DonationRequest.objects.create(
                    donor=request.user,
                    description=form.cleaned_data["description"],
                )
                DonationOrgan.objects.bulk_create([
                    DonationOrgan(
                        donation_request=application,
                        organ=organ,
                    )
                    for organ in form.cleaned_data["organs"]
                ])

            messages.success(request, "Donation application successfully submitted.")
            return redirect("donor-dashboard")

    else:
        form = DonationApplicationForm()

    return render(request, "donor/donation_application.html", {"form": form},)


@login_required
def my_applications(request):
    if request.user.role != User.Role.DONOR:
        messages.error(request, "Only donors can access their applications.")
        return redirect("donor-dashboard")

    applications = (
        DonationRequest.objects
        .filter(donor=request.user)
        .prefetch_related("organs")
        .order_by("-submitted_at")
    )

    return render(
        request,
        "donor/my_applications.html",
        {"applications": applications},
    )


def _is_verified_hospital(user):
    if not user.is_authenticated or user.role != User.Role.HOSPITAL:
        return False
    try:
        return (
            user.hospital_profile.verification_status
            == HospitalProfile.VerificationStatus.VERIFIED
        )
    except HospitalProfile.DoesNotExist:
        return False


@login_required
def hospital_application_list(request):
    if not _is_verified_hospital(request.user):
        messages.error(request, "Verified hospital account needed for access.")
        return redirect("hospital-login")

    applications = (
        DonationRequest.objects
        .filter(assigned_hospital=request.user)
        .select_related("donor")
        .prefetch_related("organs")
        .order_by("-submitted_at")
    )

    search_query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "").strip()

    if search_query:
        search_filter = (
            Q(donor__username__icontains=search_query)
            | Q(donor__first_name__icontains=search_query)
            | Q(donor__last_name__icontains=search_query)
            | Q(donor__email__icontains=search_query)
            | Q(organs__organ__icontains=search_query)
        )
        if search_query.isdigit():
            search_filter |= Q(pk=int(search_query))
        applications = applications.filter(search_filter).distinct()

    valid_statuses = DonationRequest.Status.values
    if selected_status in valid_statuses:
        applications = applications.filter(status=selected_status)
    else:
        selected_status = ""

    paginator = Paginator(applications, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "applications": page_obj.object_list,
        "search_query": search_query,
        "selected_status": selected_status,
        "status_choices": DonationRequest.Status.choices,
        "total_assigned": DonationRequest.objects.filter(
            assigned_hospital=request.user
        ).count(),
    }

    return render(request, "hospital/applications/list.html", context,)


@login_required
def hospital_application_detail(request, pk):
    if not _is_verified_hospital(request.user):
        messages.error(request, "Verified hospital account needed for access.")
        return redirect("hospital-login")
    # Only applications assigned to this hospital can be accessed.
    application = get_object_or_404(
        DonationRequest.objects
        .filter(assigned_hospital=request.user)
        .select_related("donor")
        .prefetch_related("organs"),
        pk=pk,
    )
    # Formal review history belonging to this hospital.
    reviews = (
        DonationReview.objects
        .filter(
            donation_request=application,
            hospital=request.user,
        )
        .order_by("-reviewed_at")
    )
    # Private notes belonging to this hospital.
    internal_notes = (
        HospitalApplicationNote.objects
        .filter(
            donation_request=application,
            hospital=request.user,
        )
        .order_by("-created_at")
    )

    if request.method == "POST":
        action = request.POST.get("action", "review").strip()
        # Add internal note
        if action == "add_note":
            note_text = request.POST.get("note", "").strip()

            if not note_text:
                messages.error(request, "Enter a note before saving.")
            else:
                HospitalApplicationNote.objects.create(
                    donation_request=application,
                    hospital=request.user,
                    note=note_text,
                )
                messages.success(request, "Internal note saved successfully.")
            return redirect("hospital-application-detail", pk=application.pk,)
        # RECORD FORMAL REVIEW
        elif action == "review":
            decision = request.POST.get("decision", "").strip()
            comments = request.POST.get("comments", "").strip()

            valid_decisions = DonationReview.Decision.values
            if decision not in valid_decisions:
                messages.error(request, "Select valid review decision.")
                return redirect("hospital-application-detail", pk=application.pk,)

            with transaction.atomic():
                DonationReview.objects.create(
                    donation_request=application,
                    hospital=request.user,
                    decision=decision,
                    comments=comments,
                )

                application.status = decision
                application.save(
                    update_fields=["status", "updated_at"]
                )
            messages.success(request, "Review recorded successfully.")
            return redirect("hospital-application-detail", pk=application.pk)
        else:
            messages.error(request, "Invalid application action.")
            return redirect("hospital-application-detail", pk=application.pk)

    context = {
        "application": application,
        "reviews": reviews,
        "internal_notes": internal_notes,
        "decision_choices": DonationReview.Decision.choices,
    }
    return render(request, "hospital/applications/detail.html", context)



