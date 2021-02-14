from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.builds_index_view, name="builds_index"),
    path("<int:page_number>/", views.builds_index_view, name="builds_index"),
    path("t/", views.teams_index_view, name="teams_index"),
    path("t/<int:page_number>/", views.teams_index_view, name="teams_index"),
    path(
        "create/",
        views.create_build_character_selection_view,
        name="create_build_character_selection",
    ),
    path(
        "t/create/",
        views.create_team_view,
        name="create_team",
    ),
    path(
        "create/skill-selection/",
        views.create_build_skill_item_selection_view,
        name="create_build_skill_item_selection",
    ),
    path(
        "edit/<slug:build_slug>/",
        views.create_build_skill_item_selection_view,
        name="create_build_skill_item_selection",
    ),
    path(
        "t/edit/<slug:team_slug>/",
        views.create_team_view,
        name="create_team",
    ),
    path("view/<slug:build_slug>/", views.get_build_view, name="get_build"),
    path("t/view/<slug:team_slug>/", views.get_team_view, name="get_team"),
    path(
        "delete/<slug:build_slug>/",
        views.delete_build_version_view,
        name="delete_build",
    ),
    path(
        "t/delete/<slug:team_slug>/",
        views.delete_team_view,
        name="delete_team",
    ),
    path(
        "delete-all/<slug:build_slug>/",
        views.delete_all_build_versions_view,
        name="delete_all_build",
    ),
    path("search/", views.search_build_view, name="search_build"),
    path("t/search/", views.search_team_view, name="search_team"),
    path(
        "search/results/", views.search_build_results_view, name="search_build_results"
    ),
    path(
        "t/search/results/", views.search_team_results_view, name="search_team_results"
    ),
    path(
        "search/results/<int:page_number>/",
        views.search_build_results_view,
        name="search_build_results",
    ),
    path(
        "t/search/results/<int:page_number>/",
        views.search_team_results_view,
        name="search_team_results",
    ),
    path(
        "builds-autocomplete/",
        views.BuildAutocomplete.as_view(),
        name="build-autocomplete",
    ),
]