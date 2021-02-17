from django.contrib import admin

from .models import ItemModel, MaterialModel, RaceModel


class RaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("race", "material")


admin.site.register(RaceModel, RaceAdmin)
admin.site.register(MaterialModel, MaterialAdmin)
admin.site.register(ItemModel, ItemAdmin)
