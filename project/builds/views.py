import json

from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core import serializers

from .models import BuildModel
from characters.models import SkillTypeModel, SkillModel, CharacterModel
from items.models import ItemModel

from .forms import BuildSelectionForm
from .utils import get_selected_skills, check_form_values


def create_build_character_selection_view(request):
    characters = CharacterModel.objects.all().values("slug", "name", "img")

    context = {"characters": characters}
    return render(request, "create_build_character_selection.html", context)


def create_build_skill_item_selection_view(request, build_slug=""):
    if request.method == "POST":
        try:
            char_slug = request.POST["char_slug"]
            character = CharacterModel.objects.get(slug=char_slug)
        except CharacterModel.DoesNotExist:
            return redirect("oops")

        error_message = ""
        skills = SkillModel.objects.filter(owner__slug=char_slug).select_related(
            "owner", "stype"
        )
        items = ItemModel.objects.all().select_related("race", "material")

        build_form = BuildSelectionForm(
            request.POST, char_slug=char_slug, skills=skills, items=items
        )

        if build_form.is_valid():
            build_save = build_form.save(request=request, char_slug=char_slug)

            if build_save != "This build name already exists.":
                request.session["build_created"] = True
                return redirect("/build/{}".format(build_save))
            error_message = build_save

    elif request.method == "GET":
        build = BuildModel.objects.get(slug=build_slug)

    else:
        return redirect("oops")
    context = {
        "build_form": build_form,
        "character": character,
        "skills": serializers.serialize("json", skills, use_natural_foreign_keys=True),
        "items": serializers.serialize("json", items, use_natural_foreign_keys=True),
        "error_message": error_message,
    }

    return render(request, "create_build_skill_item_selection.html", context)


def get_build_view(request, build_slug):
    build = BuildModel.objects.get(slug=build_slug)
    build_creation_message = ""

    if request.session["build_created"]:
        build_creation_message = "Build has been created."
        request.session["build_created"] = ""

    context = {"build": build, "build_creation_message": build_creation_message}

    return render(request, "get_build.html", context)


def delete_build_view(request, build_slug):
    try:
        build = BuildModel.objects.get(slug=build_slug)
    except BuildModel.DoesNotExist:
        return redirect("oops")

    # Delete build only if the user is the owner
    if build.creator == request.user:
        build.delete()
        return render(request, "build_deleted.html")