from django.contrib import admin

from .models import BuildModel


class BuildModelAdmin(admin.ModelAdmin):
    model = BuildModel

    def get_queryset(self, request):
        print(
            super(BuildModelAdmin, self)
            .get_queryset(request)
            .select_related(
                "skill_1",
                "skill_2",
                "skill_3",
                "skill_4",
                "skill_5",
                "skill_6",
                "item_1",
                "item_2",
                "item_3",
                "item_4",
                "item_5",
                "item_6",
                "item_7",
                "item_8",
            )
        )
        return (
            super(BuildModelAdmin, self)
            .get_queryset(request)
            .select_related(
                "skill_1",
                "skill_2",
                "skill_3",
                "skill_4",
                "skill_5",
                "skill_6",
                "item_1",
                "item_2",
                "item_3",
                "item_4",
                "item_5",
                "item_6",
                "item_7",
                "item_8",
            )
        )


admin.site.register(BuildModel, BuildModelAdmin)
