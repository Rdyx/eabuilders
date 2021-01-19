from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import redirect

from .models import BuildModel

from characters.models import SkillModel, CharacterModel

from .utils import get_selected_skills, check_form_values

# class BuildSelectionForm(forms.Form):
#     def __init__(self, *args, skills, items, **kwargs):
#         super(BuildSelectionForm, self).__init__(*args, **kwargs)
#         skills = skills.values_list("id", "name")
#         items = items.values_list("id", "name")

#         self.fields["skill_1"] = forms.ChoiceField(choices=skills)
#         self.fields["skill_2"] = forms.ChoiceField(choices=skills)
#         self.fields["skill_3"] = forms.ChoiceField(choices=skills)
#         self.fields["skill_4"] = forms.ChoiceField(choices=skills)
#         self.fields["skill_5"] = forms.ChoiceField(choices=skills)
#         self.fields["skill_6"] = forms.ChoiceField(choices=skills)

#         self.fields["item_1"] = forms.ChoiceField(choices=items)
#         self.fields["item_2"] = forms.ChoiceField(choices=items)
#         self.fields["item_3"] = forms.ChoiceField(choices=items)
#         self.fields["item_4"] = forms.ChoiceField(choices=items)
#         self.fields["item_5"] = forms.ChoiceField(choices=items)
#         self.fields["item_6"] = forms.ChoiceField(choices=items)
#         self.fields["item_7"] = forms.ChoiceField(choices=items)
#         self.fields["item_8"] = forms.ChoiceField(choices=items)

#     def clean(self):
#         print(self.fields)
#         super(BuildSelectionForm, self).clean()


class BuildSelectionForm(forms.Form):
    name = forms.CharField(max_length=100)
    notes = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, char_slug, skills, items, **kwargs):
        super(BuildSelectionForm, self).__init__(*args, **kwargs)
        self.skills = skills
        self.items = items
        self.skills_values = self.skills.values_list("id", "name")
        self.items_values = self.items.values_list("id", "name")

        self.fields["char_slug"] = forms.CharField(
            initial=char_slug, widget=forms.HiddenInput(attrs={"readonly": True})
        )

        self.fields["skill_1"] = forms.ChoiceField(choices=self.skills_values)
        self.fields["skill_1"] = forms.ChoiceField(choices=self.skills_values)
        self.fields["skill_2"] = forms.ChoiceField(choices=self.skills_values)
        self.fields["skill_3"] = forms.ChoiceField(choices=self.skills_values)
        self.fields["skill_4"] = forms.ChoiceField(choices=self.skills_values)
        self.fields["skill_5"] = forms.ChoiceField(choices=self.skills_values)
        self.fields["skill_6"] = forms.ChoiceField(choices=self.skills_values)

        self.fields["item_1"] = forms.ChoiceField(choices=self.items_values)
        self.fields["item_2"] = forms.ChoiceField(choices=self.items_values)
        self.fields["item_3"] = forms.ChoiceField(choices=self.items_values)
        self.fields["item_4"] = forms.ChoiceField(choices=self.items_values)
        self.fields["item_5"] = forms.ChoiceField(choices=self.items_values)
        self.fields["item_6"] = forms.ChoiceField(choices=self.items_values)
        self.fields["item_7"] = forms.ChoiceField(choices=self.items_values)
        self.fields["item_8"] = forms.ChoiceField(choices=self.items_values)

    def save(self, *args, request, char_slug, **kwargs):
        # Verify data integrity
        post_dict = dict(request.POST)
        build_name = self.cleaned_data["name"]
        try:
            character = CharacterModel.objects.get(slug=char_slug)
            build_exists = BuildModel.objects.filter(name=build_name).exists()
            selected_skill_are_valid = check_form_values(post_dict, "skill", 6)
            selected_items_are_valid = check_form_values(post_dict, "items", 8)
        except CharacterModel.DoesNotExist or selected_skill_are_valid or selected_items_are_valid:
            redirect("oops")

        if not build_exists:
            build = BuildModel()

            build.creator = request.user
            build.name = build_name
            build.slug = slugify(build_name)
            build.notes = self.cleaned_data["notes"]
            build.char = character
            build.skill_1 = self.skills.filter(id=self.cleaned_data["skill_1"]).first()
            build.skill_2 = self.skills.filter(id=self.cleaned_data["skill_2"]).first()
            build.skill_3 = self.skills.filter(id=self.cleaned_data["skill_3"]).first()
            build.skill_4 = self.skills.filter(id=self.cleaned_data["skill_4"]).first()
            build.skill_5 = self.skills.filter(id=self.cleaned_data["skill_5"]).first()
            build.skill_6 = self.skills.filter(id=self.cleaned_data["skill_6"]).first()
            build.item_1 = self.items.filter(id=self.cleaned_data["item_1"]).first()
            build.item_2 = self.items.filter(id=self.cleaned_data["item_2"]).first()
            build.item_3 = self.items.filter(id=self.cleaned_data["item_3"]).first()
            build.item_4 = self.items.filter(id=self.cleaned_data["item_4"]).first()
            build.item_5 = self.items.filter(id=self.cleaned_data["item_5"]).first()
            build.item_6 = self.items.filter(id=self.cleaned_data["item_6"]).first()
            build.item_7 = self.items.filter(id=self.cleaned_data["item_7"]).first()
            build.item_8 = self.items.filter(id=self.cleaned_data["item_8"]).first()

            build.save()
            return build.slug
        else:
            return "This build name already exists."
