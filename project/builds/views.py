import json
import re

from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import BuildModel
from characters.models import SkillTypeModel, SkillModel, CharacterModel
from items.models import ItemModel

from .forms import BuildSelectionForm
from .utils import get_selected_skills, check_form_values


@login_required
def create_build_character_selection_view(request):
    characters = CharacterModel.objects.all().values("slug", "name", "img")

    context = {"characters": characters}
    return render(request, "create_build_character_selection.html", context)


@login_required
def create_build_skill_item_selection_view(request, build_slug=""):
    items = ItemModel.objects.all().select_related("race", "material")
    error_message = ""

    if request.method == "POST":
        try:
            char_slug = request.POST["char_slug"]
            character = CharacterModel.objects.get(slug=char_slug)
        except CharacterModel.DoesNotExist:
            return redirect("oops")

        skills = SkillModel.objects.filter(owner__slug=char_slug).select_related(
            "owner", "stype"
        )

        build_form = BuildSelectionForm(
            request.POST, char_slug=char_slug, skills=skills, items=items
        )

        if build_form.is_valid():
            build_save = build_form.save(request=request, char_slug=char_slug)

            if build_save != "This build name is already taken.":
                request.session["build_created"] = True
                return redirect("/build/view/{}".format(build_save))

            error_message = build_save

    elif request.method == "GET":
        try:
            build = BuildModel.objects.select_related(
                "creator",
                "char",
                "skill_1",
                "skill_2",
                "skill_3",
                "skill_4",
                "skill_5",
                "skill_6",
                "item_1__race",
                "item_1__material",
                "item_2__race",
                "item_2__material",
                "item_3__race",
                "item_3__material",
                "item_4__race",
                "item_4__material",
                "item_5__race",
                "item_5__material",
                "item_6__race",
                "item_6__material",
                "item_7__race",
                "item_7__material",
                "item_8__race",
                "item_8__material",
            ).get(slug=build_slug)
        except BuildModel.DoesNotExist:
            return redirect("oops")

        character = CharacterModel.objects.get(slug=build.char)
        skills = SkillModel.objects.filter(owner=character).select_related(
            "owner", "stype"
        )
        skills_form_choices = skills.values_list("id", "name")
        items_form_choices = items.values_list("id", "name")
        build_form = BuildSelectionForm()
        build_form.fields["char_slug"].initial = build.char

        for field in build._meta.get_fields():
            field_name = field.name
            field_value = getattr(build, field_name)

            if field_name in build_form.fields:
                build_form.fields[field_name].initial = field_value

            if "skill" in field_name:
                build_form.fields[field_name].choices = skills_form_choices
            if "item" in field_name:
                build_form.fields[field_name].choices = items_form_choices
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


@login_required
def delete_build_view(request, build_slug):
    # Delete version number to get only build name
    build_name = re.sub(r"-\d*", "", build_slug)

    try:
        builds = BuildModel.objects.filter(name=build_name)
    except BuildModel.DoesNotExist:
        return redirect("oops")

    # Delete build only if the user is the owner
    if builds[0].creator == request.user:
        builds.delete()
        return render(request, "build_deleted.html")

    return redirect("oops")
