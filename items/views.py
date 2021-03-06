from django.shortcuts import render, redirect

from eabuilders.utils import tiers_colors
from .models import RaceModel, MaterialModel, ItemModel


def races_index_view(request):
    races = RaceModel.objects.all().order_by("name")
    context = {"races": races}
    return render(request, "races_index.html", context)


def materials_index_view(request):
    materials = MaterialModel.objects.all().order_by("name")
    context = {"materials": materials}
    return render(request, "materials_index.html", context)


def items_index_view(request):
    items = (
        ItemModel.objects.all()
        .select_related("race", "material")
        .order_by("tier", "name")
    )
    context = {"items": items, "tiers_colors": tiers_colors}
    return render(request, "items_index.html", context)


def show_race_view(request, race_slug):
    try:
        race = RaceModel.objects.get(slug=race_slug)
        related_items = ItemModel.objects.filter(race=race).order_by("tier", "name")
    except RaceModel.DoesNotExist:
        return redirect("oops")

    context = {
        "race": race,
        "related_items": related_items,
        "tiers_colors": tiers_colors,
    }
    return render(request, "race.html", context)


def show_material_view(request, material_slug):
    try:
        material = MaterialModel.objects.get(slug=material_slug)
        related_items = ItemModel.objects.filter(material=material).order_by(
            "tier", "name"
        )
    except MaterialModel.DoesNotExist:
        return redirect("oops")

    context = {
        "material": material,
        "related_items": related_items,
        "tiers_colors": tiers_colors,
    }
    return render(request, "material.html", context)


def show_item_view(request, item_slug):
    try:
        item = ItemModel.objects.select_related("race", "material").get(slug=item_slug)
    except ItemModel.DoesNotExist:
        return redirect("oops")

    context = {"item": item, "tiers_colors": tiers_colors}
    return render(request, "item.html", context)
