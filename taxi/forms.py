from django import forms
from django.core.exceptions import ValidationError

from .models import Driver, Car


def validate_license(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License must have 8 characters")

    if (
        not license_number[:3].isalpha()
        or not license_number[:3].isupper()
    ):
        raise ValidationError(
            "First 3 must be uppercase letters"
        )

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 must be digits")

    return license_number


class DriverCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password",
        )

    def clean_license_number(self) -> str:
        return validate_license(
            self.cleaned_data["license_number"]
        )

    def save(self, commit: bool = True):
        driver = super().save(commit=False)
        driver.set_password(self.cleaned_data["password"])
        if commit:
            driver.save()
        return driver


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return validate_license(
            self.cleaned_data["license_number"]
        )


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
