from django.urls import include, path

from . import views

urlpatterns = [
    path("register/", views.user_signup_view, name="register"),
    path("profile/<str:username>/", views.user_profile_page, name="profile_page"),
    path("edit-profile/", views.user_edit_view, name="user_edit"),
    path("login/", views.user_login_view, name="login"),
    path("logout/", views.user_logout_view, name="logout"),
    path("delete/<str:username>/", views.user_delete, name="user_delete"),
]
