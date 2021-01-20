from django.contrib import admin
from .models import NewsModel


class NewsModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(NewsModel, NewsModelAdmin)
