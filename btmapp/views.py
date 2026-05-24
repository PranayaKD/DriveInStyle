# btmapp/views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import (
    UserForm, 
    UserProfileForm, 
    UserUpdateForm, 
    UserProfileUpdateForm,
)
import logging

logger = logging.getLogger(__name__)


def registration(request):
    """
    User registration view with improved error handling and user feedback
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                
                messages.success(
                    request, 
                    f'Registration successful! Welcome {user.username}. Please login to continue.'
                )
                logger.info(f"New user registered: {user.username}")
                return redirect('login')
                
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                messages.error(
                    request, 
                    'An error occurred during registration. Please try again.'
                )
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
            if profile_form.errors:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
    else:
        form = UserForm()
        profile_form = UserProfileForm()
    
    context = {
        "form": form,
        'profile_form': profile_form,
    }
    
    return render(request, "registration.html", context)


def user_login(request):
    """
    User login view with improved security and error messages
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, "login.html", {})
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                logger.info(f"User logged in: {username}")
                
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account has been disabled.')
                logger.warning(f"Inactive user login attempt: {username}")
        else:
            messages.error(request, 'Invalid username or password.')
            logger.warning(f"Failed login attempt for username: {username}")
    
    return render(request, "login.html", {})


def home(request):
    """
    Home page view - accessible to all users.
    """
    context = {
        'user': request.user,
    }
    return render(request, "home.html", context)


@login_required(login_url='login')
def user_logout(request):
    """
    User logout view
    """
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye {username}! You have been logged out successfully.')
    logger.info(f"User logged out: {username}")
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    """
    User profile view
    """
    try:
        user_profile = request.user.profile
    except AttributeError:
        messages.error(request, 'Profile not found. Please contact support.')
        return redirect('home')
    
    context = {
        'user': request.user,
        'profile': user_profile,
    }
    return render(request, "profile.html", context)


@login_required(login_url='login')
def update(request):
    """
    User profile update view with improved error handling
    """
    try:
        user_profile = request.user.profile
    except AttributeError:
        messages.error(request, 'Profile not found. Please contact support.')
        return redirect('home')
    
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=user_profile
        )
        
        if form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    profile_form.save()
                
                messages.success(request, 'Your profile has been updated successfully!')
                logger.info(f"Profile updated: {request.user.username}")
                return redirect('profile')
            except Exception as e:
                logger.error(f"Profile update error: {str(e)}")
                messages.error(request, 'An error occurred while updating your profile.')
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
            if profile_form.errors:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=user_profile)
    
    context = {
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, "update.html", context)