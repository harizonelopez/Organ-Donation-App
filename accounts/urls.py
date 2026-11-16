from django.urls import path
from . import views

urlpatterns = [
    path("donor-register/", views.donor_register, name="donor-register"),
    path("donor-login/", views.donor_login, name="donor-login"),
    path("donor-logout/", views.donor_logout, name="donor-logout"),
    path("donor-dashboard/", views.donor_dashboard, name="donor-dashboard"),

    path("hospital-register/", views.hospital_register, name="hospital-register"),
    path("hospital-login/", views.hospital_login, name="hospital-login"),
    path("hospital-dashboard/", views.hospital_dashboard, name="hospital-dashboard"),
    path("hospital-logout/", views.hospital_logout, name="hospital-logout"),
]


