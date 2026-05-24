# btmapp/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),
    
    # Authentication
    path("register/", views.registration, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    
    # User Profile
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.update, name="update"),
    
    # Password Reset (Django built-in with email token verification)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name='password_reset/password_reset_form.html',
            email_template_name='password_reset/password_reset_email.html',
            subject_template_name='password_reset/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset/password_reset_done.html'
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset/password_reset_confirm.html',
            success_url='/password-reset-complete/'
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset/password_reset_complete.html'
        ),
        name="password_reset_complete",
    ),
]