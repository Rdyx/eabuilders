from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import redirect

from django_quill.fields import QuillFormField

from .models import BuildModel

from characters.models import SkillModel, CharacterModel

from .utils import get_selected_skills, check_form_values

User = get_user_model()


class BuildSelectionForm(forms.Form):
    name = forms.CharField(max_length=100)
    notes = QuillFormField(max_length=500)
    skill_1 = forms.ChoiceField(choices=[])
    skill_1 = forms.ChoiceField(choices=[])
    skill_2 = forms.ChoiceField(choices=[])
    skill_3 = forms.ChoiceField(choices=[])
    skill_4 = forms.ChoiceField(choices=[])
    skill_5 = forms.ChoiceField(choices=[])
    skill_6 = forms.ChoiceField(choices=[])
    item_1 = forms.ChoiceField(choices=[])
    item_2 = forms.ChoiceField(choices=[])
    item_3 = forms.ChoiceField(choices=[])
    item_4 = forms.ChoiceField(choices=[])
    item_5 = forms.ChoiceField(choices=[])
    item_6 = forms.ChoiceField(choices=[])
    item_7 = forms.ChoiceField(choices=[])
    item_8 = forms.ChoiceField(choices=[])

    class Meta:
        fields = "__all__"

    def __init__(self, *args, char_slug="", skills=None, items=None, **kwargs):
        super(BuildSelectionForm, self).__init__(*args, **kwargs)
        self.skills = skills
        self.items = items

        if skills:
            self.skills_values = self.skills.values_list("id", "name")
            self.fields["skill_1"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_1"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_2"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_3"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_4"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_5"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_6"] = forms.ChoiceField(choices=self.skills_values)
        if items:
            self.items_values = self.items.values_list("id", "name")
            self.fields["item_1"] = forms.ChoiceField(choices=self.items_values)
            self.fields["item_2"] = forms.ChoiceField(choices=self.items_values)
            self.fields["item_3"] = forms.ChoiceField(choices=self.items_values)
            self.fields["item_4"] = forms.ChoiceField(choices=self.items_values)
            self.fields["item_5"] = forms.ChoiceField(choices=self.items_values)
            self.fields["item_6"] = forms.ChoiceField(choices=self.items_values)
            self.fields["item_7"] = forms.ChoiceField(choices=self.items_values)
            self.fields["item_8"] = forms.ChoiceField(choices=self.items_values)

        self.fields["char_slug"] = forms.CharField(
            initial=char_slug, widget=forms.HiddenInput(attrs={"readonly": True})
        )

    def save(self, *args, request, char_slug, **kwargs):
        # Verify data integrity
        post_dict = dict(request.POST)
        build_name = self.cleaned_data["name"]
        try:
            character = CharacterModel.objects.get(slug=char_slug)
            builds = BuildModel.objects.filter(name=build_name).select_related(
                "creator",
                "char",
                "skill_1",
                "skill_2",
                "skill_3",
                "skill_4",
                "skill_5",
                "skill_6",
                "item_1",
                "item_2",
                "item_3",
                "item_4",
                "item_5",
                "item_6",
                "item_7",
                "item_8",
            )
            build_version = builds.count() + 1
            selected_skill_are_valid = check_form_values(post_dict, "skill", 6)
            selected_items_are_valid = check_form_values(post_dict, "items", 8)
        except CharacterModel.DoesNotExist or selected_skill_are_valid or selected_items_are_valid:
            redirect("oops")

        if build_version > 1 and builds[0].creator != request.user:
            return "This build name is already taken."

        build = BuildModel()

        build.creator = request.user
        build.name = build_name
        build.version = build_version
        build.slug = slugify("{}-{}".format(build_name, build_version))
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
