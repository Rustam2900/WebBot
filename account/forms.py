from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label='Full Name')

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'password1', 'password2')


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
