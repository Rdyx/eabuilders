from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


from .models import BuildModel


class CreateBuildForm(forms.ModelForm):
    class Meta:
        model = BuildModel
        fields = "__all__"
