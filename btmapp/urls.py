
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registration/", views.registeration, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("update/", views.update, name="update"),
    path("passwordreset/", views.passwordreset, name="passwordreset"),
]
