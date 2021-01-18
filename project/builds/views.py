import json

from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core import serializers

from characters.models import CharacterModel

from .forms import CreateBuildForm

# Create your views here.
def create_build_view(request):
    return redirect("create_build_character_selection")
    chars = serializers.serialize(
        "json",
        CharacterModel.objects.select_related(
            "char_skill_1__skill_type",
            "char_skill_2__skill_type",
            "char_skill_3__skill_type",
            "char_skill_4__skill_type",
            "char_skill_5__skill_type",
            "char_skill_6__skill_type",
            "char_skill_7__skill_type",
            "char_skill_8__skill_type",
            "char_skill_9__skill_type",
        ).all(),
        fields=["char_skill_1"],
    )

    context = {"form": CreateBuildForm, "chars": chars}
    return render(request, "create_build.html", context)


def create_build_character_selection_view(request):
    characters = CharacterModel.objects.all().values(
        "char_slug", "char_name", "char_img"
    )
    context = {"form": CreateBuildForm, "characters": characters}
    return render(request, "create_build_character_selection.html", context)