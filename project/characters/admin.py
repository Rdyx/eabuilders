from django.contrib import admin

from .models import SkillLevelModel, SkillTypeModel, SkillModel, CharacterModel


class CharacterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(SkillLevelModel)
admin.site.register(SkillTypeModel)
admin.site.register(SkillModel)
admin.site.register(CharacterModel, CharacterAdmin)