from django.urls import include, path

from . import views

urlpatterns = [
    path("create/", views.create_build_view, name="create_build"),
    path(
        "create/character-selection",
        views.create_build_character_selection_view,
        name="create_build_character_selection",
    ),
    path(
        "create/skill-selection",
        views.create_build_skill_selection_view,
        name="create_build_skill_selection",
    ),
    path(
        "create/items-selection",
        views.create_build_items_selection_view,
        name="create_build_items_selection",
    ),
]
