from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.builds_index_view, name="builds_index"),
    path("<int:page_number>/", views.builds_index_view, name="builds_index"),
    path(
        "create/",
        views.create_build_character_selection_view,
        name="create_build_character_selection",
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
    path("view/<slug:build_slug>/", views.get_build_view, name="get_build"),
    path(
        "delete/<slug:build_slug>/",
        views.delete_build_version_view,
        name="delete_build",
    ),
    path(
        "delete-all/<slug:build_slug>/",
        views.delete_all_build_versions_view,
        name="delete_all_build",
    ),
    path("search/", views.search_build_view, name="search_build"),
    path(
        "search/results/", views.search_build_results_view, name="search_build_results"
    ),
    path(
        "search/results/<int:page_number>/",
        views.search_build_results_view,
        name="search_build_results",
    ),
]