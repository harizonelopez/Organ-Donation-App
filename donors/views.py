from django.shortcuts import render, redirect
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


# Create your views here.

def wedonate(request):
    if request.POST:
        pass  # Skip for the time being
    return render(request, "index.html")


def donor_register(request):
    if request.POST:
        user = User()
        user.username = request.POST.get("username", "")
        user.set_password(request.POST.get("password", ""))
        user.email = request.POST.get("email", "")
        user.first_name = request.POST.get("donor_name", "")
        user.city = request.POST.get("city", "")
        user.province = request.POST.get("province", "")
        user.country = request.POST.get("country", "")
        user.contact_number = request.POST.get("contact_number", "")
        user.is_staff = False
        user.save()
        return redirect("donor-login")

    return render(request, "donor-registration.html")

def donor_login(request):
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if not user.is_staff:
                    login(request, user)
                    print(request.user, "Hello, Welcome Abord.")
                    return redirect(request.POST.get("next", "donor-landing-page"))
        else:
            msg = "Invalid password!"
            fail = 1
            return render(request, "donor-login.html", {"fail": fail, "msg": msg})

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
    provinces = [  #  Future modifications to be done for the city names to dynamically be pulled from the database
        "Nairobi",
        "Naivasha"
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


def send_mail(  #  The email function to be worked on and its settings together with the {.env} file
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
            return redirect("donor-home")
        except Exception as e:
            traceback.print_exc()
            messages.error(request, "Error updating donation request.")
            return redirect("donor-home")
        
    return render(request, "new-donation-request.html")


def book_appointment(request):
    if request.POST:
        print(request.POST.get("hospital-name", ""))
        apmt = Appointments()
        apmt.donation_request = DonationRequests.objects.get(
            id=int(request.POST.get("dreq", ""))
        )
        apmt.hospital = User.objects.get(
            hospital_name=request.POST.get("hospital-name", "")
        )
        apmt.date = request.POST.get("date", "")
        apmt.time = request.POST.get("time", "")
        apmt.appointment_status = "Pending"
        apmt.save()
        return redirect("donor-home")

    donors = DonationRequests.objects.filter(donor=request.user.id)
    users = User.objects.filter(is_staff=True)
    return render(request, "book-appointment.html", {"users": users, "donors": donors})

