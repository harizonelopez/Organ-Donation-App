# Models Registration.

from django.contrib import admin
from .models import DonationRequests, Appointments

admin.site.register(DonationRequests)
admin.site.register(Appointments)
