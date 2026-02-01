# btmapp/urls.py
from django.urls import path
from . import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),
    
    # Authentication
    path("register/", views.registeration, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    
    # User Profile
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.update, name="update"),
    
    # Password Management
    path("password-reset/", views.passwordreset, name="passwordreset"),
]