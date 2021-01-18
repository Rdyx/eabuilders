from django.urls import include, path

from . import views

urlpatterns = [
    path("create/", views.create_build_view, name="create_build"),
]
