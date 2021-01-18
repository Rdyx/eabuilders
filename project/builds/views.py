from django.shortcuts import render

from .forms import CreateBuildForm

# Create your views here.
def create_build_view(request):
    context = {"form": CreateBuildForm}
    return render(request, "create_build.html", context)
