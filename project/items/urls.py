from django.urls import include, path

from . import views

urlpatterns = [
    path("r/<int:race_id>/", views.show_race_view, name="material"),
    path("m/<int:material_id>/", views.show_material_view, name="race"),
    path("i/<int:item_id>/", views.show_item_view, name="item"),
]
