from django.urls import path
from . import views

urlpatterns = [
    path(
        "hospital/schedule/<int:application_id>/",
        views.hospital_schedule_appointment,
        name="hospital-schedule-appointment",
    ),
    path(
        "hospital/appointments/",
        views.hospital_appointment_list,
        name="hospital-appointment-list",
    ),
    path(
        "hospital/appointments/<int:appointment_id>/complete/",
        views.hospital_complete_appointment,
        name="hospital-complete-appointment",
    ),
    path(
        "hospital/appointments/<int:appointment_id>/cancel/",
        views.hospital_cancel_appointment,
        name="hospital-cancel-appointment",
    ),
]