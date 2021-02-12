import json
import re

from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.text import slugify

from eabuilders.utils import get_pagination, tiers_colors
from characters.models import SkillTypeModel, SkillModel, CharacterModel
from items.models import ItemModel

from .models import BuildModel
from .forms import BuildSelectionForm, SearchBuildForm
from .utils import (
    get_base_buildmodel_request,
    get_selected_skills,
    check_form_values,
    get_char_skills,
    get_build_sets_bonus,
)


def builds_index_view(request, page_number=1):
    pagination = 1
    total_builds, previous_page, next_page = get_pagination(
        pagination, BuildModel.objects.all(), page_number
    )

    builds = get_base_buildmodel_request().order_by("-id")[
        pagination * (page_number - 1) : page_number * pagination
    ]

    context = {
        "builds": builds,
        "total_builds": total_builds,
        "pagination": pagination,
        "previous_page": previous_page,
        "current_page": page_number,
        "next_page": next_page,
    }
    return render(request, "builds_index.html", context)


@login_required
def create_build_character_selection_view(request):
    characters = CharacterModel.objects.all().values("slug", "name", "img", "rarity")

    context = {"characters": characters, "tiers_colors": tiers_colors}
    return render(request, "create_build_character_selection.html", context)


@login_required
def create_build_skill_item_selection_view(request, build_slug=""):
    items = ItemModel.objects.all().select_related("race", "material")
    error_message = ""
    edit = False

    if request.method == "POST":
        try:
            char_slug = request.POST["char_slug"]
            character = CharacterModel.objects.get(slug=char_slug)
        except CharacterModel.DoesNotExist:
            return redirect("oops")

        skills = get_char_skills(char_slug)

        build_form = BuildSelectionForm(
            request.POST, char_slug=char_slug, skills=skills, items=items
        )

        if build_form.is_valid():
            build_save = build_form.save(request=request, char_slug=char_slug)

            if type(build_save) == dict and (
                build_save["name"] == request.POST["name"]
            ):
                request.session["build_created"] = True
                return redirect("/builds/view/{}".format(build_save["slug"]))

            error_message = build_save

    elif request.method == "GET":
        try:
            build = get_base_buildmodel_request().get(slug=build_slug)
            edit = True
        except BuildModel.DoesNotExist:
            return redirect("oops")

        character = CharacterModel.objects.get(slug=build.char.slug)
        skills = get_char_skills(character.slug)

        skills_form_choices = list(skills.values_list("id", "name"))
        items_form_choices = items.values_list("id", "name")
        build_form = BuildSelectionForm()
        build_form.fields["char_slug"].initial = build.char.slug

        for field in build._meta.get_fields():
            field_name = field.name
            field_value = getattr(build, field_name)

            if field_name in build_form.fields:
                build_form.fields[field_name].initial = field_value

            if "skill" in field_name:
                build_form.fields[field_name].choices = skills_form_choices
                build_form.fields[field_name].initial = build.__dict__[
                    field_name + "_id"
                ]
            if "item" in field_name:
                build_form.fields[field_name].choices = items_form_choices
                build_form.fields[field_name].initial = build.__dict__[
                    field_name + "_id"
                ]
    else:
        return redirect("oops")

    context = {
        "edit": edit,
        "build_form": build_form,
        "character": character,
        "skills": serializers.serialize("json", skills, use_natural_foreign_keys=True),
        "items": serializers.serialize("json", items, use_natural_foreign_keys=True),
        "tiers_colors": json.dumps(tiers_colors),  # JS usage
        "error_message": error_message,
    }

    return render(request, "create_build_skill_item_selection.html", context)


def get_build_view(request, build_slug):
    prev_build_version = False
    next_build_version = False
    last_build_version = False

    try:
        build = get_base_buildmodel_request().get(slug=build_slug)
        build_versions_list = list(
            BuildModel.objects.filter(name=build.name)
            .all()
            .order_by("version")
            .values_list("slug", flat=True)
        )
        build_sets_bonus = get_build_sets_bonus(build)

    except BuildModel.DoesNotExist:
        return redirect("oops")

    build_creation_message = ""
    build_created = request.session.get("build_created", None)

    if build_created:
        build_creation_message = "Build has been created."
        request.session["build_created"] = ""

    # Looks like empty quills fields are still generating something
    if build.notes.html == "<p><br></p>":
        build.notes = {}

    # If build has multiple versions
    if len(build_versions_list) > 1:
        current_build_version_index = build_versions_list.index(build.slug)
        # If current version is last
        if current_build_version_index + 1 == len(build_versions_list):
            next_build_version = False
        else:
            last_build_version = build_versions_list[len(build_versions_list) - 1]
            next_build_version = build_versions_list[current_build_version_index + 1]

        if build.version > 1:
            prev_build_version = build_versions_list[current_build_version_index - 1]

    context = {
        "build": build,
        "build_creation_message": build_creation_message,
        "prev_build_version": prev_build_version,
        "next_build_version": next_build_version,
        "last_build_version": last_build_version,
        "build_sets_bonus": build_sets_bonus,
    }

    return render(request, "build_details.html", context)


@login_required
def delete_build_version_view(request, build_slug):
    try:
        build = BuildModel.objects.filter(slug=build_slug)
    except BuildModel.DoesNotExist:
        return redirect("oops")

    # Delete build only if the user is the owner
    if len(build) > 0 and build[0].creator == request.user:
        build.delete()
        return render(
            request,
            "build_deleted.html",
            {"delete_status": "This build's version have been deleted."},
        )

    return redirect("oops")


@login_required
def delete_all_build_versions_view(request, build_slug):
    try:
        build = BuildModel.objects.filter(slug=build_slug)
        if build:
            related_builds = BuildModel.objects.filter(name=build[0].name)

    except BuildModel.DoesNotExist:
        return redirect("oops")

    # Delete related_builds only if the user is the owner
    if len(build) > 0 and build[0].creator == request.user:
        related_builds.delete()
        return render(
            request,
            "build_deleted.html",
            {"delete_status": "All build's versions have been deleted."},
        )

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
    total_builds_found, previous_page, next_page = get_pagination(
        pagination, builds_found, page_number
    )

    builds_found = builds_found.order_by("-id")[
        pagination * (page_number - 1) : page_number * pagination
    ]

    context = {
        "search_params": query_dict.urlencode(),  # Transfer search params to pagination
        "builds_found": builds_found,
        "pagination": pagination,
        "total_builds_found": total_builds_found,
        "previous_page": previous_page,
        "current_page": page_number,
        "next_page": next_page,
    }

    return render(request, "build_search_results.html", context)
