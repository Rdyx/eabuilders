from django.shortcuts import render


def oops_view(request):
    return render(request, "common/oops.html")
