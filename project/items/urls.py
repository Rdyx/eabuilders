from django.urls import include, path

from . import views

urlpatterns = [
    path("r/", views.races_index_view, name="races_index"),
    path("r/<slug:race_slug>/", views.show_race_view, name="race"),
    path("m/", views.materials_index_view, name="materials_index"),
    path("m/<slug:material_slug>/", views.show_material_view, name="material"),
    path("i/", views.items_index_view, name="items_index"),
    path("i/<slug:item_slug>/", views.show_item_view, name="item"),
]
