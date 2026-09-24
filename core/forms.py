# core/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Users, Services, Service, ServiceProvider, ServiceDocument
import re
from .models import Service, MenuItem

class ServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        exclude = ["provider", "is_approved"]  # Provider is set automatically, is_approved by admin
        labels = {
            "name": "Name",
            "type": "Type",
            "description": "Description",
            "price": "Service Price (₹)",
            "address": "Address",
            "phone": "Phone",
            "open_time": "Opening Time",
            "close_time": "Closing Time",
            "image": "Service Image"
        }     
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter service name"
            }),
            "type": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Enter service description"}),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter base service price",
                "step": "0.01",
                "min": "0"
            }),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Address"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Phone Number"}),
            "open_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),
            "close_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),
            "image": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"})
        }

    # Extra backend validations for robustness
    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone and not re.fullmatch(r"[0-9]{10}", phone):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Price cannot be negative.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name", "").strip()
        service_type = cleaned_data.get("type", "").strip()

        if not name:
            self.add_error("name", "Service name is required.")

        if not service_type:
            self.add_error("type", "Please select a service type.")

        return cleaned_data


class ServiceProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ["name", "phone", "address"]
        labels = {
            "name": "Full Name",
            "phone": "Phone Number",
            "address": "Address"
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3})
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise ValidationError("Name is required.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not re.fullmatch(r"[0-9]{10}", phone):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get("address", "").strip()
        if not address:
            raise ValidationError("Address is required.")
        return address





class UsersForm(forms.ModelForm):

    conform = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter confirm password",
            }
        ),
        required=True
    )

    photo = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Users
        fields = ["name", "email", "phone", "password", "adress", "status", "gender", "photo"]

        labels = {
            "password": "Password",
            "photo": "Profile Picture",
            "name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "adress": "Address",
            "status": "Status",
            "gender": "Gender",
        }

        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number"}),
            "adress": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter address"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "gender": forms.RadioSelect(attrs={"class": "form-check-input"}),
        }

    # -----------------------------
    # VALIDATIONS
    # -----------------------------

    # Validate email unique
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Users.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    # Validate phone format
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not re.fullmatch(r"[0-9]{10}", phone):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

    # Validate password + confirm password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        conform = cleaned_data.get("conform")

        if password != conform:
            self.add_error("conform", "Passwords do not match!")

        if password and len(password) < 6:
            self.add_error("password", "Password must be at least 6 characters long.")

        return cleaned_data

    # Validate image size
    def clean_photo(self):
        photo = self.cleaned_data.get("photo")

        if not photo:
            raise ValidationError("Profile picture is required.")

        if photo.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("Image size must be less than 2 MB.")

        return photo


# ------------------------------------------------------
# User Profile Edit Form (Dashboard)
# ------------------------------------------------------
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["name", "email", "phone", "adress", "gender", "photo"]
        labels = {
            "name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "adress": "Address",
            "gender": "Gender",
            "photo": "Profile Picture",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number"}),
            "adress": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter address"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user_id = None
        instance = kwargs.get("instance")
        if instance is not None and instance.pk:
            self.user_id = instance.pk
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Users.objects.filter(email=email)
        if self.user_id:
            qs = qs.exclude(pk=self.user_id)
        if qs.exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not re.fullmatch(r"[0-9]{10}", phone):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        # Photo is optional on profile edit; validate size if provided
        if photo and photo.size > 2 * 1024 * 1024:
            raise ValidationError("Image size must be less than 2 MB.")
        return photo


# ------------------------------------------------------
# Services Form
# ------------------------------------------------------
class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ["service_name", "providers"]
        widgets = {
            "service_name": forms.Textarea(attrs={"class": "form-control", "rows": 1, "placeholder": "Enter Service name"}),
            "providers": forms.SelectMultiple(attrs={"class": "form-select", "multiple": "multiple"}),
        }

    def clean_service_name(self):
        name = self.cleaned_data.get("service_name", "").strip()
        if not name:
            raise ValidationError("Service name is required.")
        return name


# ------------------------------------------------------
# Login Form
# ------------------------------------------------------
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Enter Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )
    password = forms.CharField(
        label="Enter Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email:
            self.add_error("email", "Email is required.")
        if not password:
            self.add_error("password", "Password is required.")

        return cleaned_data

