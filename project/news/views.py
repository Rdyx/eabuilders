from django.shortcuts import render

from .models import NewsModel


def news_view(request, news_slug):
    news = NewsModel.objects.select_related("author").get(slug=news_slug)

    context = {"news": news}
    return render(request, "news.html", context)
