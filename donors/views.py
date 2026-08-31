from django.shortcuts import render, redirect, get_object_or_404
from hospitals.models import User
from .models import DonationRequests
from django.contrib.auth import login, logout, authenticate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import random
from .models import DonationRequests, Appointments
from django.contrib import messages
import traceback


def wedonate(request):
    if request.POST:
        pass  
    return render(request, "index.html")


def donor_register(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username", "")
            raw_password = request.POST.get("password", "")
            email = request.POST.get("email", "")
            donor_name = request.POST.get("donor_name", "")
            city = request.POST.get("city", "")
            province = request.POST.get("province", "")
            country = request.POST.get("country", "")
            contact_number = request.POST.get("contact_number", "")

            user = User.objects.create_user(
                username=username,
                password=raw_password,
                email=email,
                first_name=donor_name
            )
            user.city = city
            user.province = province
            user.country = country
            user.contact_number = contact_number
            user.is_staff = False
            user.save()

            # Auto-login feature after registration
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                # messages.success(request, "Registration successful. You are now logged in.")
                return redirect("donor-landing-page")

            messages.info(request, "Could not log you in after registration.")
            return redirect("donor-login")

        except Exception as e:
            traceback.print_exc()
            messages.warning(request, "Registration failed. Please try again.")
            return redirect("donor-register")

    return render(request, "donor-registration.html")


def donor_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                if not user.is_staff:
                    messages.success(request, f"Welcome back, {user.first_name}!")
                    login(request, user)
                    return redirect(request.POST.get("next", "donor-home"))
                else:
                    messages.error(request, "Access denied. You are not a donor.")
            else:
                messages.error(request, "Your account is inactive.")
        else:
            # If authentication fails => Show an error message
            messages.warning(request, "Incorrect username or password.")

    return render(request, "donor-login.html")


def donor_profile_update(request):
    success = 0
    msg = 0
    pfcheck = 0
    pscheck = 0
    if "profile" in request.POST:
        user = User.objects.get(id=request.user.id)
        user.email = request.POST.get("email", "")
        user.first_name = request.POST.get("donor_name", "")
        user.city = request.POST.get("city", "")
        user.province = request.POST.get("province", "")
        user.contact_number = request.POST.get("contact", "")
        user.save()
        success = 1
        pfcheck = 1
        msg = "User Profile Updated!"
    elif "password" in request.POST:
        user = authenticate(
            username=request.user.username,
            password=request.POST.get("old_password", ""),
        )
        if user is not None:
            user.set_password(request.POST.get("new_password", ""))
            user.save()
            success = 1
            pscheck = 1
            msg = "Password changed!"
        else:
            success = 1
            pscheck = 1
            msg = "Invalid password"
    donor = User.objects.get(id=request.user.id)
    provinces = [  # [List of cities in Kenya] to be used as provinces for the donor profile
        "Nairobi",
        "Naivasha",
        "Mombasa",
        "Kisumu",
        "Nakuru",
        "Eldoret",
        "Thika",
        "Kakamega",
        "Kisii",
        "Meru",
        "Nyeri",
        "Embu",
        "Kitale",
        "Garissa",
        "Kericho",
        "Naivasha",
    ]
    provinces = [1 if donor.province is not None else 0 for i in provinces]

    return render(
        request,
        "donor-profile-update.html",
        {
            "provinces": provinces,
            "donor": donor,
            "success": success,
            "msg": msg,
            "pfcheck": pfcheck,
            "pscheck": pscheck,
        },
    )


def send_mail(  #  The email function to be worked on and its settings together with the {.env} file ---> future upgrades
    send_from,
    send_to,
    subject,
    body_of_msg,
    files=[],
    server="localhost",
    port=587,
    username="harizonelopez23@gmail.com",
    password="xkfu aslr yswq bdbt",
    use_tls=True,
):
    message = MIMEMultipart()
    message["From"] = send_from
    message["To"] = send_to
    message["Date"] = formatdate(localtime=True)
    message["Subject"] = subject
    message.attach(MIMEText(body_of_msg))
    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, message.as_string())
    smtp.quit()


def donor_forgot_password(request):
    success = 0
    if request.POST:
        username = request.POST.get("username", "")
        try:
            user = User.objects.get(username=username)
            email = user.email
            password = random.randint(1000000, 999999999999)
            send_mail(
                "harizonelopez23@gmail.com",
                email,
                "Password reset for your organ donation account",
                """Your request to change password has been received and processed.\nThis is your new password: {}\n
                            If you wish to modify the password, please go to your user profile and change it.""".format(
                    password
                ),
                server="smtp.gmail.com",
                username="harizonelopez23@gmail.com",
                password="xkfu aslr yswq bdbt",
            )
            user.set_password(password)
            user.save()
            success = 1
            msg = "Success, Check your registered email for new password!"
            return render(
                request, "donor-forgot-password.html", {"success": success, "msg": msg}
            )
        except:
            success = 1
            msg = "User does not exist!"
            return render(
                request, "donor-forgot-password.html", {"success": success, "msg": msg}
            )

    return render(request, "donor-forgot-password.html", {"success": success})


def donor_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("donor-login")


def donor_landing_page(request):
    return render(request, "donor_landing_page.html")


def donor_home(request):
    donor_requests = DonationRequests.objects.filter(donor=request.user)
    for donor_request in donor_requests:
        try:
            donor_request.datetime = donor_request.request_datetime.strftime(
                "%b %d, %Y %H:%M:%S"
            )
            status = Appointments.objects.get(
                donation_request=donor_request
            ).appointment_status
        except Exception as e:
            status = "Not Booked"
        donor_request.appointment_status = status
    return render(request, "donor-home.html", {"donationrequests": donor_requests})


def new_donation_request(request):
    if request.method == "POST":
        try:
            donation_request = DonationRequests()
            donation_request.donation_request = request.POST.get("newdonationreq", "")
            donation_request.organ_type = request.POST.get("organ_type", "")
            donation_request.blood_type = request.POST.get("blood_type", "")
            donation_request.family_relation = request.POST.get("family_relation", "")
            donation_request.family_relation_name = request.POST.get(
                "family_relation_name", ""
            )
            donation_request.family_contact_number = request.POST.get(
                "family_contact_number", ""
            )
            donation_request.donation_status = "Pending"
            donation_request.donor = request.user
            donation_request.upload_medical_doc = request.FILES.get("file", "")
            donation_request.family_consent = request.POST.get("family_consent", "")
            donation_request.donated_before = request.POST.get("donated_before", "")
            donation_request.save()
            messages.success(request, "Donation request created successfully.")
            return redirect("donor-home")
        except Exception as e:
            print(e)
            messages.warning(request, "Error updating donation request.")
            return redirect("donor-home")
        
    return render(request, "new-donation-request.html")


def book_appointment(request):
    if request.method == "POST":
        try:
            # Validate donation request ID
            dreq_id = request.POST.get("dreq")
            if not dreq_id or not dreq_id.isdigit():
                messages.warning(request, "Invalid donation request.")
                return redirect("book-appointment")

            # Create appointment object
            apmt = Appointments()
            apmt.donation_request = DonationRequests.objects.get(id=int(dreq_id))

            # Default hospital setup
            default_hospital_name = "Nairobi Hospital"

            hospital_user = User.objects.filter(
                hospital_name__iexact=default_hospital_name
            ).first()

            # Auto-create the hospital user if not found
            if not hospital_user:
                hospital_user = User.objects.create_user(
                    username="nairobi_hospital",
                    password="securepassword123",  # You can change or randomize this
                    hospital_name=default_hospital_name
                )

            # Assign hospital to appointment
            apmt.hospital = hospital_user  # ForeignKey field
            apmt.date = request.POST.get("date", "")
            apmt.time = request.POST.get("time", "")
            apmt.appointment_status = "Pending"
            apmt.save()

            messages.success(request, "Appointment booked successfully.")
            return redirect("donor-home")

        except Exception as e:
            traceback.print_exc()
            messages.warning(request, f"Error booking appointment: {str(e)}")
            return redirect("book-appointment")

    # GET request - show donation requests for current donor
    donors = DonationRequests.objects.filter(donor=request.user)
    return render(request, "book-appointment.html", {"donors": donors})

