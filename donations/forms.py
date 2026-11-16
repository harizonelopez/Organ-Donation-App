from django import forms
from .models import DonationOrgan


class DonationApplicationForm(forms.Form):
    organs = forms.MultipleChoiceField(
        choices=DonationOrgan.Organ.choices,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={
            "required": "Please select at least one organ."
        }
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 5,
            "placeholder": (
                "Share any additional information about your "
                "wishes or application (optional)."
            ),
        }),
    )

    def clean_organs(self):
        organs = self.cleaned_data["organs"]

        if not organs:
            raise forms.ValidationError(
                "Please select at least one organ."
            )

        return organs


