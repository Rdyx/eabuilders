from django.shortcuts import render, redirect

from eabuilders.utils import tiers_colors
from .models import RaceModel, MaterialModel, ItemModel


def races_index_view(request):
    races = RaceModel.objects.all()
    context = {"races": races}
    return render(request, "races_index.html", context)


def materials_index_view(request):
    materials = MaterialModel.objects.all()
    context = {"materials": materials}
    return render(request, "materials_index.html", context)


def items_index_view(request):
    items = ItemModel.objects.all().select_related("race", "material").order_by("tier")
    context = {"items": items, "tiers_colors": tiers_colors}
    return render(request, "items_index.html", context)


def show_race_view(request, race_slug):
    try:
        race = RaceModel.objects.get(slug=race_slug)
    except RaceModel.DoesNotExist:
        return redirect("oops")

    context = {"race": race}
    return render(request, "race.html", context)


def show_material_view(request, material_slug):
    try:
        material = MaterialModel.objects.get(slug=material_slug)
    except MaterialModel.DoesNotExist:
        return redirect("oops")

    context = {"material": material}
    return render(request, "material.html", context)


def show_item_view(request, item_slug):
    try:
        item = ItemModel.objects.select_related("race", "material").get(slug=item_slug)
    except ItemModel.DoesNotExist:
        return redirect("oops")

    context = {"item": item, "tiers_colors": tiers_colors}
    return render(request, "item.html", context)
