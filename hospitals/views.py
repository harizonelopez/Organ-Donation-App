from django.shortcuts import render
import pdfkit
from django.conf import settings
from django.db.models import Q
from donors.models import DonationRequests, Appointments
import json
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, logout, authenticate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, COMMASPACE
import random
from donors.models import DonationRequests, Appointments
from django.http import HttpResponse
from io import BytesIO, StringIO
from PyPDF2 import PdfFileMerger, PdfFileReader
from django.contrib import messages
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()

def home(request):
    if request.POST:
        pass
    return render(request, "hospital-main-page.html")


def search_donations(request):
    if request.POST:
        pass
    else:
        search_keyword = request.GET.get('keyword', '')
        status = "Approved"
        # Search for donations based on organ type, blood type or donor name
        donations = DonationRequests.objects.filter((Q(organ_type__iexact=search_keyword) | 
                                                     Q(blood_type__startswith=search_keyword) | 
                                                     Q(donor__first_name__iexact=search_keyword) | 
                                                     Q(donor__last_name__iexact=search_keyword)) & 
                                                     Q(donation_status__iexact=status))
        print(donations)  # Debigging purpose
        # Search for donations based on donation id
        if not donations:
            if search_keyword.isdigit():
                donations = DonationRequests.objects.filter(Q(id=int(search_keyword)) & Q(donation_status__iexact=status))

        donation_list = []
        for donation in donations:
            print(donation.donation_status)  # Debbuging purpose
            temp_dict = {}
            temp_dict["donor"] = f"{donation.donor.first_name} {donation.donor.last_name}"
            temp_dict["organ"] = donation.organ_type
            temp_dict["donation_id"] = donation.id
            temp_dict["blood_group"] = donation.blood_type
            donation_list.append(temp_dict)
        search_list = json.dumps(donation_list)
        print("Hy", search_list)  # Debbuging purpose
        return HttpResponse(search_list)


def search_donation_details(request):
    if request.POST:
        pass
    else:
        # Fetching donation details from the database
        donation_id_from_UI = request.GET.get('donation_id', '')
        donations = Appointments.objects.filter(Q(donation_request__id=int(donation_id_from_UI)))
        donation_list = []
        for donation in donations:
            temp_dict = {}
            # Donor details
            temp_dict["user_name"] = donation.donation_request.donor.username
            temp_dict["first_name"] = donation.donation_request.donor.first_name
            temp_dict["last_name"] = donation.donation_request.donor.last_name
            temp_dict["email"] = donation.donation_request.donor.email
            temp_dict["contact_number"] = donation.donation_request.donor.contact_number
            temp_dict["city"] = donation.donation_request.donor.city
            temp_dict["country"] = donation.donation_request.donor.country
            temp_dict["province"] = donation.donation_request.donor.province  
            # Donation details
            temp_dict["organ"] = donation.donation_request.organ_type
            temp_dict["donation_id"] = donation.donation_request.id
            temp_dict["blood_group"] = donation.donation_request.blood_type
            temp_dict["donation_status"] = donation.donation_request.donation_status
            temp_dict["approved_by"] = donation.hospital.hospital_name
            temp_dict["family_member_name"] = donation.donation_request.family_relation_name
            temp_dict["family_member_relation"] = donation.donation_request.family_relation
            temp_dict["family_member_contact"] = donation.donation_request.family_contact_number
            donation_list.append(temp_dict)
        donation_details = json.dumps(donation_list)

        return HttpResponse(donation_details)


def fetch_appointments(request):
    if request.method == "POST":
        pass
    else:
        print("Fetching appointments from db...")  # For debugging purpose
        status = "Pending"
        appointments = Appointments.objects.filter(Q(hospital__id__iexact=request.user.id) & Q(appointment_status__iexact=status))
        
        appointment_list = []
        for appointment in appointments:
            temp_dict = {}
            temp_dict["first_name"] = appointment.donation_request.donor.first_name
            temp_dict["last_name"] = appointment.donation_request.donor.last_name
            # Donation details
            temp_dict["organ"] = appointment.donation_request.organ_type
            temp_dict["donation_id"] = appointment.donation_request.id
            temp_dict["blood_group"] = appointment.donation_request.blood_type
            # Appointment details
            temp_dict["appointment_id"] = appointment.id
            temp_dict["date"] = appointment.date
            temp_dict["time"] = appointment.time
            temp_dict["appointment_status"] = appointment.appointment_status
            appointment_list.append(temp_dict)
        appointment_details = json.dumps(appointment_list)
        return HttpResponse(appointment_details)


def fetch_donations(request):
    if request.POST:
        pass
    else:
        donation_status = "Pending"
        appointment_status = "Approved"
        appointments = Appointments.objects.filter(Q(hospital__id__iexact=request.user.id) & Q(appointment_status__iexact=appointment_status) & Q(donation_request__donation_status__iexact=donation_status))
        appointment_list = []
        for appointment in appointments:
            temp_dict = {}
            temp_dict["first_name"] = appointment.donation_request.donor.first_name
            temp_dict["last_name"] = appointment.donation_request.donor.last_name
            # Donation details
            temp_dict["organ"] = appointment.donation_request.organ_type
            temp_dict["donation_id"] = appointment.donation_request.id
            temp_dict["blood_group"] = appointment.donation_request.blood_type
            # Appointment details
            temp_dict["appointment_id"] = appointment.id
            temp_dict["date"] = appointment.date
            temp_dict["time"] = appointment.time
            temp_dict["appointment_status"] = appointment.appointment_status
            appointment_list.append(temp_dict)
        appointment_details = json.dumps(appointment_list)

        return HttpResponse(appointment_details)
    

def hospital_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('hospital-register')

        try:
            user = User(
                username=username,
                email=email,
                hospital_name=request.POST.get("hospital_name"),
                city=request.POST.get("city"),
                province=request.POST.get("province"),
                country=request.POST.get("country"),
                contact_number=request.POST.get("contact_number"),
                is_active=True,
                is_staff=True
            )
            user.set_password(password)
            user.save()

            # Authenticate and log the user in
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')  # Change this to your actual dashboard URL name
            else:
                messages.error(request, "Authentication failed after registration.")
                return redirect('hospital-login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('hospital-register')

    return render(request, "hospital-registration.html")

def hospital_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return redirect("home")
                else:
                    messages.error(request, "Inactive account or unauthorized user!")
            else:
                messages.error(request, "Invalid username or password!")

        return render(request, "hospital-login.html")

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return render(request, "hospital-login.html")


def fetch_appointment_details(request):
    if request.POST:
        pass
    else:
        # Fetching appointment details
        appointment_id_from_UI = request.GET.get('appointment_id', '')
        print('Appointment id', appointment_id_from_UI)  # Debbuging purpose
        appointments = Appointments.objects.filter(Q(id=int(appointment_id_from_UI)))
        appointment_list = []
        for appointment in appointments:
            # Donor details
            temp_dict = {}
            temp_dict["first_name"] = appointment.donation_request.donor.first_name
            temp_dict["last_name"] = appointment.donation_request.donor.last_name
            temp_dict["email"] = appointment.donation_request.donor.email
            temp_dict["contact_number"] = appointment.donation_request.donor.contact_number
            temp_dict["city"] = appointment.donation_request.donor.city
            temp_dict["country"] = appointment.donation_request.donor.country
            temp_dict["province"] = appointment.donation_request.donor.province  
            # Donation details
            temp_dict["organ"] = appointment.donation_request.organ_type
            temp_dict["donation_id"] = appointment.donation_request.id
            temp_dict["blood_group"] = appointment.donation_request.blood_type
            temp_dict["donation_status"] = appointment.donation_request.donation_status
            temp_dict["family_member_name"] = appointment.donation_request.family_relation_name
            temp_dict["family_member_relation"] = appointment.donation_request.family_relation
            temp_dict["family_member_contact"] = appointment.donation_request.family_contact_number
            # Appointment details
            temp_dict["appointment_id"] = appointment.id
            temp_dict["date"] = appointment.date
            temp_dict["time"] = appointment.time
            temp_dict["appointment_status"] = appointment.appointment_status
            appointment_list.append(temp_dict)
        appointment_details = json.dumps(appointment_list)
        return HttpResponse(appointment_details)


def fetch_donation_details(request):
    if request.POST:
        pass
    else:
        # Fetching donation details
        donation_id_from_UI = request.GET.get('donation_id', '')
        print('Donation id', donation_id_from_UI)
        donations = DonationRequests.objects.filter(Q(id=int(donation_id_from_UI)))
        donation_list = []
        for donation in donations:
            # Donor details
            temp_dict = {}
            temp_dict["first_name"] = donation.donor.first_name
            temp_dict["last_name"] = donation.donor.last_name
            temp_dict["email"] = donation.donor.email
            temp_dict["contact_number"] = donation.donor.contact_number
            temp_dict["city"] = donation.donor.city
            temp_dict["country"] = donation.donor.country
            temp_dict["province"] = donation.donor.province 
            # Donation details
            temp_dict["organ"] = donation.organ_type
            temp_dict["donation_id"] = donation.id
            temp_dict["blood_group"] = donation.blood_type
            temp_dict["donation_status"] = donation.donation_status
            temp_dict["family_member_name"] = donation.family_relation_name
            temp_dict["family_member_relation"] = donation.family_relation
            temp_dict["family_member_contact"] = donation.family_contact_number

            donation_list.append(temp_dict)
        donation_details = json.dumps(donation_list)
        return HttpResponse(donation_details)


@csrf_exempt
def approve_appointments(request):
    if request.POST:
        appointment_id_from_UI = request.POST.get('ID', '')
        actionToPerform = request.POST.get('action', '')
        print('Appointment id', appointment_id_from_UI)  # Debbuging purposes
        print('ActionToPerform', actionToPerform)  # Debbuging purposes
        appointments = get_object_or_404(Appointments, id=appointment_id_from_UI)
        appointments.appointment_status = actionToPerform
        appointments.save(update_fields=["appointment_status"])
    return HttpResponse("success")


@csrf_exempt
def approve_donations(request):
    if request.POST:
        donation_id_from_UI = request.POST.get('ID', '')
        actionToPerform = request.POST.get('action', '')
        print('Donation id', donation_id_from_UI)  # Debbuging purpose
        print('ActionToPerform', actionToPerform)  # Debbuging purpose
        donation = get_object_or_404(DonationRequests, id=donation_id_from_UI)
        donation.donation_status = actionToPerform
        donation.save(update_fields=["donation_status"])
    return HttpResponse("success")


def fetch_counts(request): 
    if request.POST:
        pass
    else:
        print(request.user.hospital_name)  # Debbuging purpose
        appointment_count = Appointments.objects.filter(Q(hospital__hospital_name__iexact=request.user.hospital_name) & Q(appointment_status__iexact="Pending")).count()
        print("Appointment count", appointment_count)  # Debbuging purpose
        donation_status = "Pending"
        appointment_status = "Approved"
        donation_count = Appointments.objects.filter(Q(hospital__hospital_name__iexact=request.user.hospital_name) & Q(appointment_status__iexact=appointment_status) & Q(donation_request__donation_status__iexact=donation_status)).count()
        print("Donation count", donation_count)  # Debbuging purpose
        dummy_list = []
        temp_dict = {}
        temp_dict["appointment_count"] = appointment_count
        temp_dict["donation_count"] = donation_count
        dummy_list.append(temp_dict)
        count_json = json.dumps(dummy_list)
        return HttpResponse(count_json)


def send_mail(send_from, send_to, subject, body_of_msg, files=[],
              server="localhost", 
              port=587, 
              username='', 
              password='',
              use_tls=True):
    message = MIMEMultipart()
    message['From'] = send_from
    message['To'] = send_to
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject
    message.attach(MIMEText(body_of_msg))
    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, message.as_string())
    smtp.quit()


def hospital_forgot_password(request):
    success = 0
    if request.POST:
        username = request.POST.get("username", "")
        try:
            user = User.objects.get(username=username)
            email = user.email
            password = random.randint(1000000, 999999999999)
            user.set_password(password)
            user.save()
            send_mail("harizonelopez23@gmail.com",
                      email, "Password reset for your account", 
                      """Your request to change password has been processed.
                      \n This is your new password: {}
                      \n If you wish to change password, please go to your user profile and change it.""".format(password),
                      server="smtp.gmail.com", username="harizonelopez23@gmail.com", password="xkfu aslr yswq bdbt")
            success = 1
            msg = "Success. Check your email for new password!"
            return render(request, "hospital-forgot-password.html", {"success": success, "msg": msg})
        except:
            success = 1
            msg = "User doesn't exist!"
            return render(request, "hospital-forgot-password.html", {"success": success, "msg": msg})

    return render(request, "hospital-forgot-password.html", {"success": success})


def form_to_PDF(request, donor_id=1):

    donation_request = DonationRequests.objects.get(id=donor_id)
    user = donation_request.donor
    donations = DonationRequests.objects.filter(donor=user)
    template = get_template("user-details.html")
    html = template.render({'user': user, 'donors': donations})
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF)
    try:
        pdf = pdfkit.from_string(html, False, configuration=config)
    except Exception as e:
        print(e)  # Debbuging reason
        pass
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    userpdf = PdfFileReader(BytesIO(pdf))
    usermedicaldoc = donation_request.upload_medical_doc.read()
    usermedbytes = BytesIO(usermedicaldoc)
    usermedicalpdf = PdfFileReader(usermedbytes)
    merger = PdfFileMerger()
    merger.append(userpdf)
    merger.append(usermedicalpdf)
    merger.write(response)
    return response


def email_donor(request, donor_id=1):
    donor = DonationRequests.objects.get(id=donor_id).donor
    send_mail("harizonelopez23@gmail.com", donor.email, "Organ Donation",
              """You've been requested by {} to donate organ. Thanks!""".format(request.user.hospital_name),
              server="smtp.gmail.com", username="harizonelopez23@gmail.com", password="xkfu aslr yswq bdbt")
    return HttpResponse("Success")


def get_user_details(request):
    if request.POST:
        pass
    else:
        user_details = []
        temp_dict = {}
        hospital = User.objects.get(id=request.user.id)
        temp_dict["hospital_name"] = hospital.hospital_name
        temp_dict["hospital_email"] = hospital.email
        temp_dict["hospital_city"] = hospital.city
        temp_dict["hospital_province"] = hospital.province # To be ommitted sooner
        temp_dict["hospital_contact"] = hospital.contact_number
        user_details.append(temp_dict)
        user_json = json.dumps(user_details)
    return HttpResponse(user_json)


@csrf_exempt
def update_user_details(request):
    if request.POST:
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        city = request.POST.get('city', '')
        contact = request.POST.get('contact', '')
        province = request.POST.get('province', '')  # To be ommitted sooner

        user = User.objects.get(id=request.user.id)
        user.email = request.POST.get('email', '')
        user.hospital_name = request.POST.get('name', '')
        user.city = request.POST.get('city', '')
        user.province = request.POST.get('province', '')  # To be ommitted sooner
        user.contact_number = request.POST.get('contact', '')
        print("About to save..!")  # Debbuging purpose
        user.save()
    return HttpResponse("success")


@csrf_exempt
def update_pwd_details(request):
    if request.POST:
        user = authenticate(username=request.user.username, password=request.POST.get("old_password", ""))
        if user is not None:
            user.set_password(request.POST.get("new_password", ""))
            print("About to save password..!")  # Debbuging purpose
            user.save(update_fields=["password"])
    return HttpResponse("success")


def hospital_logout(request):
    logout(request)
    return redirect("hospital-login")

