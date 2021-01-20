from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.template import loaders

from .forms import SigninForm, EditUserForm, UserCreationForm, UserChangeForm

from .utils import get_user_builds

User = get_user_model()


def user_login_view(request):
    # If user is auth, get him to home
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            form = SigninForm(data=request.POST)
            if form.is_valid():
                user = form.signin_user()

                if user is not None and user.is_active:
                    login(request, user)

                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("/")
        else:
            form = SigninForm()

        context = {"user_form": form}

        return render(request, "login.html", context)


@login_required
def user_logout_view(request):
    logout(request)
    return redirect("/")


def user_signup_view(request):
    # If user is auth, get him to home
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")

                # Login and redirect to home
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("/")
        else:
            form = UserCreationForm()

        context = {"user_form": form}

        return render(request, "register.html", context)


def user_profile_page(request, username):
    # Try to get targeted user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect("oops")

    user_builds = get_user_builds(user)

    context = {"user": user, "user_builds": user_builds}
    return render(request, "profile.html", context)


@login_required
def user_edit_view(request):
    context_message = ""
    user = User.objects.get(username=request.user)

    if request.method == "POST":
        edit_user_form = EditUserForm(request.POST, instance=user)

        if edit_user_form.is_valid():
            edit_user_form.save()
            context_message = "Your profile has been edited."
    else:
        edit_user_form = EditUserForm(instance=user)

    context = {
        "user": user,
        "edit_user_form": edit_user_form,
        "context_message": context_message,
    }
    return render(request, "user_edit.html", context)


@login_required
def user_delete(request, username):
    # Try to get targeted user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect("oops")

    # Delete user only if it's the same as logged in
    if request.user == user:
        user.delete()
        return render(request, "user_deleted.html")

    return redirect("oops")
