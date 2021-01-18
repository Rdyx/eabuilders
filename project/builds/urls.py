from django.urls import include, path

from . import views

urlpatterns = [
    path("create/", views.create_build_view, name="create_build"),
    path(
        "create/character-selection",
        views.create_build_character_selection_view,
        name="create_build_character_selection",
    ),
]
