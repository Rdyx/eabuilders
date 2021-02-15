import json
import re

from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.text import slugify

from dal import autocomplete

from eabuilders.utils import get_pagination, tiers_colors
from characters.models import SkillTypeModel, SkillModel, CharacterModel
from items.models import ItemModel

from .models import BuildModel, TeamModel
from .forms import BuildSelectionForm, SearchBuildForm, TeamCreateForm, SearchTeamForm
from .big_queries import get_base_buildmodel_request, get_team_builds_request
from .utils import (
    get_selected_skills,
    check_form_values,
    get_char_skills,
    get_build_sets_bonus,
    update_model_votes,
)


def builds_index_view(request, page_number=1):
    pagination = 10
    total_builds, previous_page, next_page = get_pagination(
        pagination, BuildModel.objects.all(), page_number
    )

    builds = (
        get_base_buildmodel_request()
        .all()
        .order_by("-id")[pagination * (page_number - 1) : page_number * pagination]
    )

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
        build_qs = get_base_buildmodel_request().filter(slug=build_slug)
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

    if request.user.is_authenticated:
        update_model_votes(request, build_qs)
    else:
        redirect("login")

    context = {
        "build": build_qs[0],
        "build_creation_message": build_creation_message,
        "prev_build_version": prev_build_version,
        "next_build_version": next_build_version,
        "last_build_version": last_build_version,
        "build_sets_bonus": build_sets_bonus,
        "build_votes": True,
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
        creator = query_dict.get("creator", "")
        name = query_dict.get("name", "")
        game_mode = query_dict.getlist("game_mode", "")
        votes = query_dict.get("votes", "")
        selected_items = query_dict.getlist("items")
        excluded_items = query_dict.getlist("exclude_items")

        if creator:
            builds_found = builds_found.filter(Q(creator__username__icontains=creator))

        if name:
            builds_found = builds_found.filter(Q(name__icontains=name))

        if len(game_mode) > 0:
            builds_found = builds_found.filter(Q(game_mode__in=game_mode))

        if votes:
            builds_found = builds_found.filter(Q(votes__gte=votes))

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

    pagination = 10
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


class BuildAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return redirect("oops")

        qs = (
            BuildModel.objects.all()
            .select_related("creator")
            .order_by("name", "version")
        )

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) | Q(creator__username__icontains=self.q)
            )

        return qs


@login_required
def create_team_view(request, team_slug=""):
    error_message = ""

    if request.method == "POST":
        team_form = TeamCreateForm(request.POST)

        if team_form.is_valid():
            # If we got a slug, it means we are editing.
            if team_slug:
                team_save = team_form.update(request=request, team_slug=team_slug)
                request.session["team_created"] = "Team has been edited."
            else:
                team_save = team_form.save(request=request)
                request.session["team_created"] = "Team has been created."

            if type(team_save) == dict and (team_save["name"] == request.POST["name"]):
                return redirect("/builds/t/view/{}".format(team_save["slug"]))

            error_message = team_save

    # Edit mode
    elif request.method == "GET" and team_slug:
        try:
            team = TeamModel.objects.get(slug=team_slug)
        except TeamModel.DoesNotExist:
            return redirect("oops")

        team_form = TeamCreateForm()

        for field in team._meta.get_fields():
            field_name = field.name
            field_value = getattr(team, field_name)

            if field_name in team_form.fields:
                team_form.fields[field_name].initial = field_value
                team_form.fields[field_name].widget.attrs["readonly"] = True

    else:
        team_form = TeamCreateForm()

    context = {"team_form": team_form, "error_message": error_message}
    return render(request, "team_create.html", context)


def get_team_view(request, team_slug):
    try:
        team = TeamModel.objects.get(slug=team_slug)
        team_qs = TeamModel.objects.filter(slug=team_slug)

        # Reducing queries time by getting each build from 3 different queries instead of 1 big
        build_1 = get_base_buildmodel_request().get(id=team.__dict__["build_1_id"])
        build_2 = get_base_buildmodel_request().get(id=team.__dict__["build_2_id"])
        build_3 = get_base_buildmodel_request().get(id=team.__dict__["build_3_id"])
    except TeamModel.DoesNotExist:
        return redirect("oops")

    team_creation_message = request.session.get("team_created", None)

    if team_creation_message:
        request.session["team_created"] = ""

    # Looks like empty quills fields are still generating something
    if team.notes.html == "<p><br></p>":
        team.notes = {}

    if request.user.is_authenticated:
        update_model_votes(request, team_qs)
    else:
        redirect("login")

    context = {
        "team": team_qs[0],
        "build_1": build_1,
        "build_2": build_2,
        "build_3": build_3,
        "team_creation_message": team_creation_message,
        "team_votes": True,
    }

    return render(request, "team_details.html", context)


def teams_index_view(request, page_number=1):
    pagination = 10
    total_teams, previous_page, next_page = get_pagination(
        pagination, TeamModel.objects.all(), page_number
    )

    teams = (
        get_team_builds_request()
        .all()
        .order_by("-id")[pagination * (page_number - 1) : page_number * pagination]
    )

    context = {
        "teams": teams,
        "total_teams": total_teams,
        "pagination": pagination,
        "previous_page": previous_page,
        "current_page": page_number,
        "next_page": next_page,
    }
    return render(request, "teams_index.html", context)


def search_team_view(request):
    chars = CharacterModel.objects.all()
    search_team_form = SearchTeamForm(chars=chars)
    context = {"search_team_form": search_team_form}
    return render(request, "team_search.html", context)


def search_team_results_view(request, page_number=1):
    query_dict = request.GET

    # Filter by char to manipulate lighter queryset
    teams_found = get_team_builds_request().all()

    # If we got filters, filter queryset
    if len(query_dict) > 0:
        creator = query_dict.get("creator", "")
        name = query_dict.get("name", "")
        game_mode = query_dict.getlist("game_mode", "")
        votes = query_dict.get("votes", "")
        selected_chars = query_dict.getlist("chars")
        excluded_chars = query_dict.getlist("exclude_chars")

        if creator:
            teams_found = teams_found.filter(Q(creator__username__icontains=creator))

        if name:
            teams_found = teams_found.filter(Q(name__icontains=name))

        if len(game_mode) > 0:
            teams_found = teams_found.filter(Q(game_mode__in=game_mode))

        if votes:
            teams_found = teams_found.filter(Q(votes__gte=votes))

        # If chars have been selected
        if len(selected_chars) > 0:
            teams_found = teams_found.filter(
                Q(build_1__char__slug__in=selected_chars)
                | Q(build_2__char__slug__in=selected_chars)
                | Q(build_3__char__slug__in=selected_chars)
            )

        # If chars have been excluded
        if len(excluded_chars) > 0:
            teams_found = teams_found.exclude(
                Q(build_1__char__slug__in=excluded_chars)
                | Q(build_2__char__slug__in=excluded_chars)
                | Q(build_3__char__slug__in=excluded_chars)
            )

    pagination = 10
    total_teams_found, previous_page, next_page = get_pagination(
        pagination, teams_found, page_number
    )

    teams_found = teams_found.order_by("-id")[
        pagination * (page_number - 1) : page_number * pagination
    ]

    context = {
        "search_params": query_dict.urlencode(),  # Transfer search params to pagination
        "teams_found": teams_found,
        "pagination": pagination,
        "total_teams_found": total_teams_found,
        "previous_page": previous_page,
        "current_page": page_number,
        "next_page": next_page,
    }

    return render(request, "team_search_results.html", context)


@login_required
def delete_team_view(request, team_slug):
    try:
        team = TeamModel.objects.filter(slug=team_slug)
    except TeamModel.DoesNotExist:
        return redirect("oops")

    # Delete related_teams only if the user is the owner
    if len(team) > 0 and team[0].creator == request.user:
        team.delete()
        return render(
            request,
            "team_deleted.html",
            {"delete_status": "Team has been deleted."},
        )

    return redirect("oops")