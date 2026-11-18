from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path("", account_views.welcome, name="welcome"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("donations/", include("donations.urls")),
    path("appointments/", include("appointments.urls")),
    path("core/", include("core.urls")),
]


