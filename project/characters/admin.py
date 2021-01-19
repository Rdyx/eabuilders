from django.contrib import admin

from .models import SkillTypeModel, SkillModel, CharacterModel


class CharacterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(SkillTypeModel)
admin.site.register(SkillModel)
admin.site.register(CharacterModel, CharacterAdmin)