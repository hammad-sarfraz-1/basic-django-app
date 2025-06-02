from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="Username")
    password = forms.CharField(max_length=128, label="Password", widget=forms.PasswordInput)
    # remember_me = forms.BooleanField(required=False, label="Remember me")
    class Meta:
        model = User
        fields = ["username", "password"]
