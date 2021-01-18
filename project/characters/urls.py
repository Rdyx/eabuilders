from django.urls import include, path

from . import views

urlpatterns = [
    path("<slug:char_slug>/", views.get_char_view, name="create_build"),
]
