from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import UserForm


def user_login_view(request):
    username = request.POST("username")
    password = request.POST("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        redirect("")


def user_logout_view(request):
    logout(request)
    return redirect("/")


def user_signup_view(request):
    # Is user is auth, get him to home
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                # Hashing pwd
                password = make_password(form.cleaned_data.get("password"))

                # Register user
                user = form.create(form.cleaned_data)
                # Login and redirect to home
                login(request, user)
                return redirect("/")
        else:
            form = UserForm()

        context = {"user_form": form}

        return render(request, "register.html", context)


def user_profile_page(request, username):
    user = User.objects.get(username=username)
    context = {"username": user}
    return render(request, "profile.html", context)
