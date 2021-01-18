import json

from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core import serializers

from characters.models import SkillTypeModel, SkillModel, CharacterModel

from .forms import CreateBuildForm, SkillSelectionForm
from .utils import get_selected_skills


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

    context = {"characters": characters}
    return render(request, "create_build_character_selection.html", context)


def create_build_skill_selection_view(request):
    if request.method == "POST":
        try:
            char_slug = request.POST["char-slug"]
            character = CharacterModel.objects.get(char_slug=char_slug)
        except CharacterModel.DoesNotExist:
            return redirect("oops")
    else:
        return redirect("oops")

    skills = SkillModel.objects.select_related("skill_type").filter(
        skill_owner=character
    )

    context = {
        "form": SkillSelectionForm(skills=skills),
        "skills": serializers.serialize("json", skills, use_natural_foreign_keys=True),
    }

    return render(request, "create_build_skill_selection.html", context)


def create_build_items_selection_view(request):
    if request.method == "POST":
        skills_list = get_selected_skills(request)
        skill_owner = skills_list[0].skill_owner.id

        # If all skill have the same owner id, get the owner
        if all(skill.skill_owner.id == skill_owner for skill in skills_list):
            try:
                character = CharacterModel.objects.get(id=skill_owner)
            except CharacterModel.DoesNotExist:
                return redirect("oops")
        else:
            return redirect("oops")
    else:
        return redirect("oops")

    skills = SkillModel.objects.select_related("skill_type").filter(
        skill_owner=character
    )

    context = {
        "form": SkillSelectionForm(skills=skills),
        "skills": serializers.serialize("json", skills, use_natural_foreign_keys=True),
    }

    return render(request, "create_build_skill_selection.html", context)