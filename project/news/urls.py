from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.news_index_view, name="news_index"),
    path("<slug:news_slug>/", views.news_view, name="news"),
]
