from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("register/", views.hospital_register, name="hospital-register"),
    path("login/", views.hospital_login, name="hospital-login"),
    path("forgot-password/", views.hospital_forgot_password, name="hospital-forgot-password"),
    path("hospital-logout/", views.hospital_logout, name="hospital-logout"),
    path("search-donations/", views.search_donations, name="search-donations"),
    path("search-donation-details/", views.search_donation_details, name="search-donation-details"),
    path("fetch-appointments/", views.fetch_appointments, name="fetch-appointments"),
    path("fetch-appointment-details/", views.fetch_appointment_details, name="fetch-appointment-details"),
    path("fetch-donations/", views.fetch_donations, name="fetch-donations"),
    path("fetch-donation-details/", views.fetch_donation_details, name="fetch-donation-details"),
    path("appointments-approval/", views.approve_appointments, name="appointments-approval"),
    path("donations-approval/", views.approve_donations, name="donations-approval"),
    path("fetch-counts/", views.fetch_counts, name="fetch-counts"),
    path("view-pdf/<int:donor_id>/", views.form_to_PDF, name="form-to-pdf"),
    path("get-user-details/", views.get_user_details, name="get-user-details"),
    path("update-user-details/", views.update_user_details, name="update-user-details"),
    path("update-pwd-details/", views.update_pwd_details, name="update-pwd-details"),
    path("email-donor/<int:donor_id>/", views.email_donor, name="email-donor"),
]
