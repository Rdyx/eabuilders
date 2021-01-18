from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def signin_user(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        return authenticate(username=username, password=password)
