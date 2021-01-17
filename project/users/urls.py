from django.urls import include, path

from . import views

urlpatterns = [
    path("register/", views.user_signup_view, name="register"),
    path("profile/<str:username>/", views.user_profile_page, name="profile_page"),
    path("logout/", views.user_logout_view, name="logout"),
]