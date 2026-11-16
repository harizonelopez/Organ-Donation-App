from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class DonorRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter email address",
        })
    )

    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 0712345678",
        })
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date",
        })
    )

    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your residential address",
        })
    )

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your city or town",
        })
    )

    country = forms.CharField(
        required=True,
        initial="Kenya",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your country",
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter first name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter last name",
            }),
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username",
            }),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"].strip()

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} form-control".strip()


class HospitalRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Official hospital email address",
        })
    )

    hospital_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter hospital name",
        })
    )

    registration_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Hospital registration number",
        })
    )

    contact_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 0712345678",
        })
    )

    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Hospital physical address",
        })
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Hospital city or town",
        })
    )

    country = forms.CharField(
        max_length=100,
        initial="Kenya",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Country",
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
        )

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a hospital username",
            }),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email

    def clean_registration_number(self):
        registration_number = (
            self.cleaned_data["registration_number"].strip()
        )

        from .models import HospitalProfile

        if HospitalProfile.objects.filter(
            registration_number__iexact=registration_number
        ).exists():
            raise forms.ValidationError(
                "This hospital registration number is already registered."
            )

        return registration_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{existing_class} form-control".strip()
            )

