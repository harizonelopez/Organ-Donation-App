from django.urls import path
from . import views

urlpatterns = [
    path(
        "new/",
        views.donation_application, 
        name="donation-application",
    ),
    path(
        "my-applications/", 
        views.my_applications, 
        name="my-applications",
    ),
     path(
        "hospital/applications/", 
        views.hospital_application_list, 
        name="hospital-application-list",
    ),
    path(
        "hospital/applications/<int:pk>/", 
        views.hospital_application_detail, 
        name="hospital-application-detail",
    ),
]


