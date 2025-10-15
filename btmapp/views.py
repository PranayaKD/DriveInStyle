# Password Reset View
from django.contrib.auth.models import User
from btmapp.forms import PasswordResetForm
from django.shortcuts import render,redirect
from btmapp.forms import UserForm,UserProfileForm,userUpdateForm,UserProfileUpdateForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def registeration(request):
    registered = False
    if request.method == "POST":
        form = UserForm(request.POST)
        form1= UserProfileForm(request.POST,request.FILES)
        
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            
            
            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        
        
    else:
        form = UserForm()
        form1= UserProfileForm()
            
            
    context = {
        "form" : form,
        'form1':form1,
        "registered" :registered
    }
    
    return render(request,"registeration.html",context)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username , password = password)
        
        if user:
            if user.is_active:
                login(request,user)
                return redirect("home")
        else:
            return HttpResponse("pls check your cred ")
    return render(request,"login.html",{})


@login_required(login_url='login') 
def home(request):
    return render(request,"home.html", {})

@login_required(login_url='login') 
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')      
def profile(request):
    return render(request,"profile.html",{}) 


@login_required(login_url='login') 
def update(request):
    if request.method == "POST":
        form = userUpdateForm(request.POST,instance = request.user)
        form1 = UserProfileUpdateForm(request.POST,request.FILES,instance = request.user.userregisteration)
        
        if form.is_valid() and form1.is_valid():
            user = form.save()
            form1.save()
            
            profile = form1.save(commit=False) 
            profile.user = user
            profile.save()
            return redirect('profile')
        
    else:
        form = userUpdateForm(instance = request.user)
        form1 = UserProfileUpdateForm(instance = request.user.userregisteration)
    return render(request,"update.html",{'form':form ,'form1':form1 })
        
def passwordreset(request):
    user_not_exist = False
    password_mismatch = False
    password_reset_success = False
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user_not_exist = True
                return render(request, 'password_reset.html', {'form': form, 'user_not_exist': user_not_exist})
            if password != confirm_password:
                password_mismatch = True
                return render(request, 'password_reset.html', {'form': form, 'password_mismatch': password_mismatch})
            user.set_password(password)
            user.save()
            password_reset_success = True
            return render(request, 'password_reset.html', {'form': PasswordResetForm(), 'password_reset_success': password_reset_success})
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})        
        
        
        
        
        
        
        
    