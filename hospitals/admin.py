# Model Registration.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("province", "hospital_name", "country", "contact_number")}),
    )


admin.site.register(User, UserAdmin)
