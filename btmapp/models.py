
# btmapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRegistration(models.Model):
    """
    Extended user profile model with address and contact information
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Contact Information
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits'
            )
        ],
        help_text="10-digit mobile number",
        blank=True,
        default=''
    )
    
    # Address Information
    door_no = models.CharField(
        max_length=20,
        help_text="Door/House number",
        blank=True,
        default=''
    )
    street = models.CharField(max_length=100, blank=True, default='')
    landmark = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Pincode must be exactly 6 digits'
            )
        ],
        blank=True,
        default=''
    )
    
    # Profile Picture
    userpic = models.ImageField(
        upload_to="profiles/%Y/%m/",
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_address(self):
        """Return formatted full address"""
        parts = [self.door_no, self.street, self.landmark, self.city, self.state]
        address = ", ".join([p for p in parts if p])
        if self.pincode:
            address += f" - {self.pincode}"
        return address or "No address provided"
    
    @property
    def display_phone(self):
        """Return formatted phone number"""
        if len(self.phone) >= 10:
            return f"+91 {self.phone[-10:-5]} {self.phone[-5:]}"
        return self.phone or "Not provided"
    
    def get_profile_picture_url(self):
        """Return profile picture URL or default"""
        if self.userpic:
            return self.userpic.url
        return '/static/images/default-avatar.png'


# Signal to create UserRegistration when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserRegistration when a new User is created.
    """
    if created:
        UserRegistration.objects.get_or_create(user=instance)