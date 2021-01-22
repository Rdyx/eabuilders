from django.shortcuts import render

from news.models import NewsModel


def index_view(request):
    # Different than news_index view, only last 5 shown
    latest_news = (
        NewsModel.objects.all()
        .select_related("author")
        .exclude(slug="about")
        .order_by("-id")[:5]
    )
    context = {"latest_news": latest_news}
    return render(request, "index.html", context)


def oops_view(request):
    return render(request, "common/oops.html")
