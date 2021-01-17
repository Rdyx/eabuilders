from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")
        # widgets = {"password": forms.PasswordInput()}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
