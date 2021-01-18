from django.shortcuts import render, redirect


from .models import RaceModel, MaterialModel, ItemModel


def show_race_view(request, race_slug):
    try:
        race = RaceModel.objects.get(race_slug=race_slug)
    except RaceModel.DoesNotExist:
        return redirect("oops")

    context = {"race": race}
    return render(request, "race.html", context)


def show_material_view(request, material_slug):
    try:
        material = MaterialModel.objects.get(material_slug=material_slug)
    except MaterialModel.DoesNotExist:
        return redirect("oops")

    context = {"material": material}
    return render(request, "material.html", context)


def show_item_view(request, item_slug):
    try:
        item = ItemModel.objects.select_related("item_race", "item_material").get(
            item_slug=item_slug
        )
    except ItemModel.DoesNotExist:
        return redirect("oops")

    context = {"item": item}
    return render(request, "item.html", context)
