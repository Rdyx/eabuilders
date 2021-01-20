from django.urls import include, path

from . import views

urlpatterns = [
    path("<slug:news_slug>/", views.news_view, name="news"),
]
