from django.urls import include, path

from . import views

urlpatterns = [
    path("r/<slug:race_slug>/", views.show_race_view, name="material"),
    path("m/<slug:material_slug>/", views.show_material_view, name="race"),
    path("i/<slug:item_slug>/", views.show_item_view, name="item"),
]
