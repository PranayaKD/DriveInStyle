# btmapp/forms.py
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UserRegistration


class UserForm(forms.ModelForm):
    """
    User registration form with password validation
    """
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        }),
        help_text='Password must be at least 8 characters long'
    )
    confirm_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        }),
        help_text='Enter the same password again'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'autocomplete': 'email'
            }),
        }
        help_texts = {
            'username': 'Letters, digits and @/./+/-/_ only.',
            'email': 'We will send important notifications to this email.',
        }
    
    def clean_username(self):
        """Validate that username is unique"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def clean_password(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password
    
    def clean(self):
        """Validate that passwords match"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    User profile form with captcha and improved widgets
    """
    captcha = ReCaptchaField()
    
    class Meta:
        model = UserRegistration
        fields = ['phone', 'door_no', 'street', 'landmark', 'city', 'state', 'pincode', 'userpic']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit phone number',
                'pattern': '[0-9]{10}',
                'maxlength': '10'
            }),
            'door_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Door/House number'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street name'
            }),
            'landmark': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nearby landmark'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '6-digit pincode',
                'pattern': '[0-9]{6}',
                'maxlength': '6'
            }),
            'userpic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        help_texts = {
            'phone': 'Enter 10-digit mobile number',
            'pincode': 'Enter 6-digit postal code',
            'userpic': 'Click or drag to upload your profile picture',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        optional_fields = ['door_no', 'street', 'landmark', 'city', 'state', 'pincode', 'userpic']
        for field in optional_fields:
            self.fields[field].required = False
        
        self.fields['phone'].required = True
    
    def clean_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) != 10:
            raise ValidationError('Phone number must be exactly 10 digits.')
        if phone and not phone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        return phone
    
    def clean_pincode(self):
        """Validate pincode"""
        pincode = self.cleaned_data.get('pincode')
        if pincode and len(pincode) != 6:
            raise ValidationError('Pincode must be exactly 6 digits.')
        if pincode and not pincode.isdigit():
            raise ValidationError('Pincode must contain only digits.')
        return pincode
    
    def clean_userpic(self):
        """Validate uploaded image"""
        userpic = self.cleaned_data.get('userpic')
        if userpic:
            if userpic.size > 5 * 1024 * 1024:
                raise ValidationError('Image file size cannot exceed 5MB.')
            
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            ext = userpic.name.lower().split('.')[-1]
            if f'.{ext}' not in valid_extensions:
                raise ValidationError(
                    f'Unsupported file type. Please use: {", ".join(valid_extensions)}'
                )
        
        return userpic


class UserUpdateForm(forms.ModelForm):
    """
    User account update form (username and email)
    """
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'readonly': 'readonly'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
    
    def clean_email(self):
        """Validate that email is unique (excluding current user)"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email is already registered to another account.')
        return email


class UserProfileUpdateForm(forms.ModelForm):
    """
    User profile update form (without captcha for updates)
    """
    class Meta:
        model = UserRegistration
        fields = ['phone', 'door_no', 'street', 'landmark', 'city', 'state', 'pincode', 'userpic']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit phone number'
            }),
            'door_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Door/House number'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street name'
            }),
            'landmark': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nearby landmark'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '6-digit pincode',
                'maxlength': '6'
            }),
            'userpic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def clean_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) != 10:
            raise ValidationError('Phone number must be exactly 10 digits.')
        return phone
    
    def clean_pincode(self):
        """Validate pincode"""
        pincode = self.cleaned_data.get('pincode')
        if pincode and len(pincode) != 6:
            raise ValidationError('Pincode must be exactly 6 digits.')
        return pincode
    
    def clean_userpic(self):
        """Validate uploaded image"""
        userpic = self.cleaned_data.get('userpic')
        if userpic and hasattr(userpic, 'size'):
            if userpic.size > 5 * 1024 * 1024:
                raise ValidationError('Image file size cannot exceed 5MB.')
        return userpic