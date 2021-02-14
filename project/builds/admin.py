from django.contrib import admin

from .models import BuildModel, TeamModel


class BuildModelAdmin(admin.ModelAdmin):
    model = BuildModel

    prepopulated_fields = {"slug": ("name", "version")}

    def get_queryset(self, request):
        return (
            super(BuildModelAdmin, self).get_queryset(request).select_related("creator")
        )


class TeamModelAdmin(admin.ModelAdmin):
    model = TeamModel

    prepopulated_fields = {"slug": ("name",)}

    raw_id_fields = ["build_1", "build_2", "build_3"]

    def get_queryset(self, request):
        return (
            super(TeamModelAdmin, self).get_queryset(request).select_related("creator")
        )


admin.site.register(BuildModel, BuildModelAdmin)
admin.site.register(TeamModel, TeamModelAdmin)
