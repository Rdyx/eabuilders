from django.shortcuts import render, redirect


from .models import RaceModel, MaterialModel, ItemModel


def show_race_view(request, race_id):
    try:
        race = RaceModel.objects.get(race_id=race_id)
    except RaceModel.DoesNotExist:
        return redirect("oops")

    context = {"race": race}
    return render(request, "race.html", context)


def show_material_view(request, material_id):
    try:
        material = MaterialModel.objects.get(material_id=material_id)
    except MaterialModel.DoesNotExist:
        return redirect("oops")

    context = {"material": material}
    return render(request, "material.html", context)


def show_item_view(request, item_id):
    try:
        item = ItemModel.objects.select_related("item_race", "item_material").get(
            item_id=item_id
        )
    except ItemModel.DoesNotExist:
        return redirect("oops")

    context = {"item": item}
    return render(request, "item.html", context)
