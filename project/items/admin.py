from django.contrib import admin

from .models import RaceModel, MaterialModel, ItemModel


class RaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"race_slug": ("race_name",)}


class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {"material_slug": ("material_name",)}


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"item_slug": ("item_name",)}


admin.site.register(RaceModel, RaceAdmin)
admin.site.register(MaterialModel, MaterialAdmin)
admin.site.register(ItemModel, ItemAdmin)
