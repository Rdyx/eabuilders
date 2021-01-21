from django.contrib import admin

from .models import BuildModel


class BuildModelAdmin(admin.ModelAdmin):
    model = BuildModel

    prepopulated_fields = {"slug": ("name", "version")}

    def get_queryset(self, request):
        return (
            super(BuildModelAdmin, self).get_queryset(request).select_related("creator")
        )


admin.site.register(BuildModel, BuildModelAdmin)
