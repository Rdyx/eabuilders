from django.contrib import admin

from .models import RaceModel, MaterialModel, ItemModel


admin.site.register(RaceModel)
admin.site.register(MaterialModel)
admin.site.register(ItemModel)
