from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

from django.contrib.auth.forms import UserCreationForm, UsernameField


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def signin_user(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        return authenticate(username=username, password=password)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        exclude = [
            "buildmodel",
            "email",
            "first_name",
            "groups",
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "last_name",
            "logentry",
            "user_permissions",
        ]

    date_joined = forms.CharField(disabled=True)
    username = forms.CharField(disabled=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
