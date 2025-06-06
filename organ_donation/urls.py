"""organ_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from donors import views as v
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('wedonate')),  # Redirect to the home page
    path('home/', v.wedonate, name='wedonate'),  # Home page route
    path('donors/', include('donors.urls')),    # Include donor's app URLs
    path('hospitals/', include('hospitals.urls')),  # Include hospital's app URLs
    path('admin/', admin.site.urls),    # Admin site route
]
