from django.shortcuts import render


def show_race_view(request, race_id):
    return render(request, "race.html", context)


def show_material_view(request, material_id):
    return render(request, "material.html", context)


def show_item_view(request, item_id):
    return render(request, "item.html", context)
