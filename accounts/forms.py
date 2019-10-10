from django import forms
# from django.forms.widgets import ClearableFileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AuthRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'password1', 'password2'
        ]
