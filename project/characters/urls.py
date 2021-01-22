from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.chars_index_view, name="chars_index"),
    path(
        "<slug:char_slug>/",
        views.get_char_view,
        name="get_char",
    ),
    path(
        "<slug:char_slug>/<str:current_skill_level>/",
        views.get_char_view,
        name="get_char_with_skill_level",
    ),
]
