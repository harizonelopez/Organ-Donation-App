from django import forms
from donations.models import DonationRequest
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "donation_request",
            "appointment_date",
            "appointment_time",
            "location",
            "hospital_notes",
        ]

        widgets = {
            "appointment_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
            "appointment_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control",
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter appointment location",
            }),
            "hospital_notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Additional instructions for the donor",
            }),
        }

    def __init__(self, *args, hospital=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["donation_request"].queryset = (
            DonationRequest.objects.filter(
                assigned_hospital=hospital
            ).select_related("donor").order_by("-submitted_at")
        )

        self.fields["donation_request"].widget.attrs.update({
            "class": "form-select",
        })



        