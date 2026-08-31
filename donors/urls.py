from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.donor_landing_page, name="donor-landing-page"),
    path("register/", views.donor_register, name="donor-register"),
    path("login/", views.donor_login, name="donor-login"),
    path("book-appointment/", views.book_appointment, name="book-appointment"),
    path("new-donation-request/", views.new_donation_request, name="new-donation-request"),
    path("donation-history/", views.donor_home, name="donor-home"),
    path("update_profile/", views.donor_profile_update, name="donor-profile-update"),
    path("forgot-password/", views.donor_forgot_password, name="donor-forgot-password"),
    path("logout/", views.donor_logout, name="donor-logout"),
]
