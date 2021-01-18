from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from characters.models import SkillModel, CharacterModel

from .models import BuildModel


class CreateBuildForm(forms.ModelForm):
    class Meta:
        model = BuildModel
        fields = ("build_name", "build_notes")

    def __init__(self, *args, **kwargs):
        super(CreateBuildForm, self).__init__(*args, **kwargs)


class SkillSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        skills = kwargs.pop("skills")
        super(SkillSelectionForm, self).__init__(*args, **kwargs)

        skills = skills.values_list("id", "skill_name")

        self.fields["skill_1"] = forms.ChoiceField(choices=skills)
        self.fields["skill_2"] = forms.ChoiceField(choices=skills)
        self.fields["skill_3"] = forms.ChoiceField(choices=skills)
        self.fields["skill_4"] = forms.ChoiceField(choices=skills)
        self.fields["skill_5"] = forms.ChoiceField(choices=skills)
        self.fields["skill_6"] = forms.ChoiceField(choices=skills)
