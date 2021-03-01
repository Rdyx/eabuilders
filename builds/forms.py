from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import redirect

from dal import autocomplete
from django_quill.fields import QuillFormField

from .models import BuildModel, TeamModel

from characters.models import SkillModel, CharacterModel

from .utils import check_form_values, format_select_items_list

User = get_user_model()


class BuildSelectionForm(forms.Form):
    name = forms.CharField(max_length=100)
    notes = QuillFormField(max_length=2000, required=False)
    game_mode = forms.ChoiceField(choices=[(i, i) for i in ["Lab", "Arena"]])
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
        exclude = ["char_slug"]

    def __init__(self, *args, char_slug="", skills=None, items=None, **kwargs):
        super(BuildSelectionForm, self).__init__(*args, **kwargs)
        self.skills = skills
        self.items = items

        if skills:
            self.skills_values = list(self.skills.values_list("id", "name"))
            self.skills_values.insert(0, ("", "No selection"))
            self.fields["skill_1"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_1"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_2"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_3"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_4"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_5"] = forms.ChoiceField(choices=self.skills_values)
            self.fields["skill_6"] = forms.ChoiceField(choices=self.skills_values)
        if items:
            self.items_values = format_select_items_list(self.items)

            self.items_values.insert(0, ("", "No selection"))
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

        if len(build_name) < 3:
            return "Your build name is too short."

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
            last_build = builds.order_by("-version").first()

            build_version = 1
            if last_build:
                build_version = last_build.version + 1

        except CharacterModel.DoesNotExist:
            redirect("oops")

        if build_version > 1 and builds[0].creator != request.user:
            return "This build name is already taken."

        selected_skill_are_valid = check_form_values(post_dict, "skill", 6, True)
        selected_items_are_valid = check_form_values(post_dict, "item", 8, False)
        if not selected_skill_are_valid or not selected_items_are_valid:
            return "A skill or an item has been selected twice."

        build = BuildModel()

        build.creator = request.user
        build.name = build_name
        build.version = build_version
        build.slug = slugify("{}-{}".format(build_name, build_version))
        build.notes = self.cleaned_data["notes"]
        build.char = character
        build.game_mode = self.cleaned_data["game_mode"]
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
        return {"name": build.name, "slug": build.slug}


# Note there's js trick to make fields non required and avoid GET request to overload url
class SearchBuildForm(forms.ModelForm):
    creator = forms.CharField(label="Build's creator name contains", required=False)
    name = forms.CharField(label="Build's name contains", required=False)
    game_mode = forms.MultipleChoiceField(
        choices=[(i, i) for i in ["Lab", "Arena"]], required=False
    )
    votes = forms.IntegerField(label="Minimum number of positive votes", required=False)

    class Meta:
        model = BuildModel
        fields = "__all__"
        exclude = [
            "version",
            "creation_date",
            "slug",
            "notes",
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
        ]

    def __init__(self, *args, items=[], **kwargs):
        super(SearchBuildForm, self).__init__(*args, **kwargs)

        self.fields["char"] = forms.ChoiceField(
            choices=CharacterModel.objects.all().values_list("slug", "name"),
            label="Build's hero",
        )

        self.items = items.values_list(
            "slug", "name", "tier", "race__name", "material__name"
        ).order_by("race", "tier", "name")

        # Formatting items list for front-end field
        items_list = []
        for item in self.items:
            items_list.append(
                [item[0], "{} (T{}, {}, {})".format(item[1], item[2], item[3], item[4])]
            )

        if items:
            self.items_values = list(items_list)
            self.items_values.insert(0, ("", "No selection"))
            self.fields["items"] = forms.MultipleChoiceField(
                choices=self.items_values, label="Build must uses item(s)", initial=""
            )
            self.fields["exclude_items"] = forms.MultipleChoiceField(
                choices=self.items_values,
                label="Build must not uses item(s)",
                initial="",
            )


class TeamCreateForm(forms.Form):
    def _get_autocomplete_field(qs, url, min_input_len):
        return forms.ModelChoiceField(
            queryset=qs,
            widget=autocomplete.ModelSelect2(
                url=url,
                attrs={
                    # Only trigger autocompletion after N characters have been typed
                    "data-minimum-input-length": min_input_len,
                },
            ),
        )

    qs = BuildModel.objects.all().select_related("creator", "char")

    name = forms.CharField(max_length=100)
    notes = QuillFormField(max_length=2000, required=False)
    game_mode = forms.ChoiceField(choices=[(i, i) for i in ["Lab", "Arena"]])

    build_1 = _get_autocomplete_field(qs, "build-autocomplete", 3)
    build_2 = _get_autocomplete_field(qs, "build-autocomplete", 3)
    build_3 = _get_autocomplete_field(qs, "build-autocomplete", 3)

    def update(self, *args, request, team_slug, **kwargs):
        team = TeamModel.objects.get(slug=team_slug)
        team.notes = self.cleaned_data["notes"]
        if team.creator == request.user:
            team.save()
            return {"name": team.name, "slug": team.slug}

    def save(self, *args, request, **kwargs):
        team_name = self.cleaned_data["name"]

        if len(team_name) < 3:
            return "Your team name is too short."

        team_exists = TeamModel.objects.filter(name=team_name).count()

        build_1 = self.cleaned_data["build_1"]
        build_2 = self.cleaned_data["build_2"]
        build_3 = self.cleaned_data["build_3"]

        if team_exists > 0:
            return "This team name is already taken."

        # If a build has been selected twice (no matter which versions)
        if build_1.name in [build_2.name, build_3.name] or build_2.name == build_3.name:
            return "A build has been selected twice (maybe with different versions?)."

        # If a hero from build is appearing twice
        if build_1.char in [build_2.char, build_3.char] or build_2.char == build_3.char:
            return "A hero from builds has been selected twice."

        team = TeamModel()

        team.creator = request.user
        team.name = team_name
        team.slug = slugify(team_name)
        team.notes = self.cleaned_data["notes"]
        team.game_mode = self.cleaned_data["game_mode"]

        team.build_1 = self.cleaned_data["build_1"]
        team.build_2 = self.cleaned_data["build_2"]
        team.build_3 = self.cleaned_data["build_3"]

        team.save()

        return {"name": team.name, "slug": team.slug}


# Note there's js trick to make fields non required and avoid GET request to overload url
class SearchTeamForm(forms.ModelForm):
    creator = forms.CharField(label="Team's creator name contains", required=False)
    name = forms.CharField(label="Team's name contains", required=False)
    game_mode = forms.MultipleChoiceField(
        choices=[(i, i) for i in ["Lab", "Arena"]], required=False
    )
    votes = forms.IntegerField(label="Minimum number of positive votes", required=False)

    class Meta:
        model = TeamModel
        fields = "__all__"
        exclude = [
            "creation_date",
            "slug",
            "notes",
            "build_1",
            "build_2",
            "build_3",
        ]

    def __init__(self, *args, chars=[], **kwargs):
        super(SearchTeamForm, self).__init__(*args, **kwargs)

        self.chars = chars.values_list("slug", "name").order_by("name")

        # Formatting items list for front-end field
        chars_list = []
        for char in self.chars:
            chars_list.append([char[0], char[1]])

        if chars:
            self.chars_values = list(chars_list)
            self.chars_values.insert(0, ("", "No selection"))
            self.fields["chars"] = forms.MultipleChoiceField(
                choices=self.chars_values, label="Build must uses hero(s)", initial=""
            )
            self.fields["exclude_chars"] = forms.MultipleChoiceField(
                choices=self.chars_values,
                label="Build must not uses hero(s)",
                initial="",
            )
