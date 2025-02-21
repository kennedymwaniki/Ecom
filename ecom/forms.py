from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=True, help_text="enter phone number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'phone_number']
