from django.shortcuts import render

from .models import NewsModel


def news_index_view(request):
    all_news = (
        NewsModel.objects.select_related("author")
        .all()
        .exclude(slug="about")
        .order_by("-id")
    )

    context = {"all_news": all_news}
    return render(request, "news_index.html", context)


def news_view(request, news_slug):
    news = NewsModel.objects.select_related("author").get(slug=news_slug)

    context = {"news": news}
    return render(request, "news.html", context)
