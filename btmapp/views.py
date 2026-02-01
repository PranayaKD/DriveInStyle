# btmapp/views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import (
    UserForm, 
    UserProfileForm, 
    userUpdateForm, 
    UserProfileUpdateForm,
    PasswordResetForm
)
import logging

logger = logging.getLogger(__name__)


def registeration(request):
    """
    User registration view with improved error handling and user feedback
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect to home
        return redirect('home')
    
    if request.method == "POST":
        form = UserForm(request.POST)
        form1 = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid() and form1.is_valid():
            try:
                # Use transaction to ensure both user and profile are created together
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    
                    profile = form1.save(commit=False)
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
            # Show specific form errors
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
            if form1.errors:
                for field, errors in form1.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
    else:
        form = UserForm()
        form1 = UserProfileForm()
    
    context = {
        "form": form,
        'form1': form1,
    }
    
    return render(request, "registeration.html", context)


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
                
                # Redirect to next page if specified, otherwise home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account has been disabled.')
                logger.warning(f"Inactive user login attempt: {username}")
        else:
            messages.error(request, 'Invalid username or password.')
            logger.warning(f"Failed login attempt for username: {username}")
    
    return render(request, "login.html", {})


@login_required(login_url='login')
def home(request):
    """
    Home page view - only accessible to logged-in users
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
        # Ensure user profile exists
        user_profile = request.user.userregisteration
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
        user_profile = request.user.userregisteration
    except AttributeError:
        messages.error(request, 'Profile not found. Please contact support.')
        return redirect('home')
    
    if request.method == "POST":
        form = userUpdateForm(request.POST, instance=request.user)
        form1 = UserProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=user_profile
        )
        
        if form.is_valid() and form1.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    form1.save()
                
                messages.success(request, 'Your profile has been updated successfully!')
                logger.info(f"Profile updated: {request.user.username}")
                return redirect('profile')
            except Exception as e:
                logger.error(f"Profile update error: {str(e)}")
                messages.error(request, 'An error occurred while updating your profile.')
        else:
            # Show form errors
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
            if form1.errors:
                for field, errors in form1.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
    else:
        form = userUpdateForm(instance=request.user)
        form1 = UserProfileUpdateForm(instance=user_profile)
    
    context = {
        'form': form,
        'form1': form1,
    }
    return render(request, "update.html", context)


def passwordreset(request):
    """
    Password reset view with improved security and validation
    
    Note: This is a basic implementation. For production, consider using
    Django's built-in password reset views with email verification.
    """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            
            # Check if passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match. Please try again.')
                return render(request, 'password_reset.html', {'form': form})
            
            # Check if user exists
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Don't reveal if username exists (security best practice)
                messages.error(request, 'Invalid username or password reset failed.')
                logger.warning(f"Password reset attempt for non-existent user: {username}")
                return render(request, 'password_reset.html', {'form': form})
            
            try:
                # Update password
                user.set_password(password)
                user.save()
                
                messages.success(
                    request, 
                    'Password reset successful! Please login with your new password.'
                )
                logger.info(f"Password reset successful for user: {username}")
                return redirect('login')
                
            except Exception as e:
                logger.error(f"Password reset error for {username}: {str(e)}")
                messages.error(request, 'An error occurred. Please try again later.')
                return render(request, 'password_reset.html', {'form': form})
        else:
            # Show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = PasswordResetForm()
    
    return render(request, 'password_reset.html', {'form': form})