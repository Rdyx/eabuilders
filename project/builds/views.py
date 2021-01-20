import json
import re

from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import BuildModel
from characters.models import SkillTypeModel, SkillModel, CharacterModel
from items.models import ItemModel

from .forms import BuildSelectionForm, SearchBuildForm
from .utils import get_base_buildmodel_request, get_selected_skills, check_form_values


def builds_index_view(request, page_number=1):
    pagination = 1
    total_builds = BuildModel.objects.all().count()
    previous_page = page_number - 1 if page_number > 1 else 0
    next_page = page_number + 1 if (page_number * pagination) < total_builds else 0

    builds = get_base_buildmodel_request().order_by("-id")[
        pagination * (page_number - 1) : page_number * pagination
    ]

    context = {
        "builds": builds,
        "total_builds": total_builds,
        "previous_page": previous_page,
        "current_page": page_number,
        "next_page": next_page,
    }
    return render(request, "builds_index.html", context)


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

        skills = SkillModel.objects.filter(
            owner__slug=char_slug, level__level="4 (Max)"
        ).select_related("owner", "stype", "level")

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
            build = get_base_buildmodel_request().get(slug=build_slug)
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


def search_build_view(request):
    items = ItemModel.objects.all().select_related("race", "material")
    search_build_form = SearchBuildForm(items=items)
    context = {"search_build_form": search_build_form}
    return render(request, "build_search.html", context)


def search_build_results_view(request, page_number=1):

    query_dict = request.GET

    # Filter by char to manipulate lighter queryset
    builds_found = get_base_buildmodel_request().filter(
        Q(char__slug__exact=query_dict.get("char", ""))
    )

    # If we got filters, filter queryset
    if len(query_dict) > 0:
        selected_items = query_dict.getlist("items")
        excluded_items = query_dict.getlist("exclude_items")
        print(selected_items, excluded_items)
        builds_found = builds_found.filter(
            Q(creator__username__icontains=query_dict.get("creator", ""))
            & Q(name__icontains=query_dict.get("name", ""))
        )

        # If items have been selected
        if len(selected_items) > 0:
            builds_found = builds_found.filter(
                Q(item_1__slug__in=selected_items)
                | Q(item_2__slug__in=selected_items)
                | Q(item_3__slug__in=selected_items)
                | Q(item_4__slug__in=selected_items)
                | Q(item_5__slug__in=selected_items)
                | Q(item_6__slug__in=selected_items)
                | Q(item_7__slug__in=selected_items)
                | Q(item_8__slug__in=selected_items)
            )

        # If items have been excluded
        if len(excluded_items) > 0:
            builds_found = builds_found.exclude(
                Q(item_1__slug__in=excluded_items)
                | Q(item_2__slug__in=excluded_items)
                | Q(item_3__slug__in=excluded_items)
                | Q(item_4__slug__in=excluded_items)
                | Q(item_5__slug__in=excluded_items)
                | Q(item_6__slug__in=excluded_items)
                | Q(item_7__slug__in=excluded_items)
                | Q(item_8__slug__in=excluded_items)
            )

    pagination = 1
    total_builds_found = builds_found.count()
    previous_page = page_number - 1 if page_number > 1 else 0
    next_page = (
        page_number + 1 if (page_number * pagination) < total_builds_found else 0
    )

    builds_found = builds_found[
        pagination * (page_number - 1) : page_number * pagination
    ]

    context = {
        "search_params": query_dict.urlencode(),  # Transfer search params to pagination
        "builds_found": builds_found,
        "total_builds_found": total_builds_found,
        "previous_page": previous_page,
        "current_page": page_number,
        "next_page": next_page,
    }

    return render(request, "build_search_results.html", context)
