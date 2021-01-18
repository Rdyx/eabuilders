from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from characters.models import CharacterModel

from .models import BuildModel


class CreateBuildForm(forms.ModelForm):
    class Meta:
        model = BuildModel
        fields = ("build_name", "build_notes")

    def __init__(self, *args, **kwargs):
        super(CreateBuildForm, self).__init__(*args, **kwargs)
