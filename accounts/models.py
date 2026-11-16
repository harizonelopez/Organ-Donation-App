from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["role"] = "ADMIN"
        return super().create_superuser(
            username,
            email=email,
            password=password,
            **extra_fields
        )    

class User(AbstractUser):
    class Role(models.TextChoices):
        DONOR = "DONOR", "Donor"
        HOSPITAL = "HOSPITAL", "Hospital"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DONOR
    )
    email = models.EmailField(unique=True)
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class DonorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="donor_profile"
    )
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Kenya")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donor Profile - {self.user.username}"


class HospitalProfile(models.Model):
    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="hospital_profile"
    )

    hospital_name = models.CharField(max_length=200)
    registration_number = models.CharField(
        max_length=100,
        unique=True
    )

    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Kenya")

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hospital_name
