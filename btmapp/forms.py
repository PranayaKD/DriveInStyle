from django import forms 
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.models import User 
from btmapp.models import UserRegisteration

class UserForm (forms.ModelForm):
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['username', 'email', 'password']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserRegisteration
        fields = ['phone', 'door_no',"street", 'landmark', 'city','state', 'pincode','userpic']
    captcha = ReCaptchaField() 


class  userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        
        
     
class UserProfileUpdateForm(forms.ModelForm):
        class Meta:
            model = UserRegisteration
            fields = ['phone', 'door_no',"street", 'landmark', 'city','state', 'pincode','userpic']
     
    
class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    

     
     
     
     
     
     
     
     
     
        

# <!DOCTYPE html>
# <html lang="en">
#   <head>
#     <meta charset="UTF-8" />
#     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#     <title>user details</title>
#   </head>
#   <body>
#     <h1>Registeration Form</h1>
#     {{ form.as_p }}
#     {{ form1.as_p }}
#     <input type="submit" value="REGISTER" />
#   </body>
# </html>