from django.contrib import admin

from .models import SkillLevelModel, SkillTypeModel, SkillModel, CharacterModel


class CharacterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SkillAdmin(admin.ModelAdmin):
    list_filter = ["owner"]
    ordering = ["owner", "name", "level"]
    list_select_related = ["owner", "stype", "level"]
    save_as = True
    search_fields = ["owner__name", "name"]


admin.site.register(SkillLevelModel)
admin.site.register(SkillTypeModel)
admin.site.register(SkillModel, SkillAdmin)
admin.site.register(CharacterModel, CharacterAdmin)