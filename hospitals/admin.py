# Hospitals admin model registration for User model with custom fields

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("province", "hospital_name", "country", "contact_number", "city")}),
    )
    list_display = ("username", "email", "hospital_name", "province", "country", "is_staff", "is_active")
    search_fields = ("username", "email", "hospital_name", "province", "country")

admin.site.register(User, CustomUserAdmin)
