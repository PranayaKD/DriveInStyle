
# btmapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRegisteration(models.Model):
    """
    Extended user profile model with address and contact information
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userregisteration'
    )
    
    # Contact Information
    phone = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(1000000000, message="Phone number must be 10 digits"),
            MaxValueValidator(9999999999, message="Phone number must be 10 digits")
        ],
        help_text="10-digit mobile number"
    )
    
    # Address Information
    door_no = models.CharField(
        max_length=20,
        help_text="Door/House number",
        blank=True,
        null=True
    )
    street = models.CharField(max_length=100, blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Pincode must be exactly 6 digits'
            )
        ],
        blank=True,
        null=True
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
        phone_str = str(self.phone)
        if len(phone_str) >= 10:
            return f"+91 {phone_str[-10:-5]} {phone_str[-5:]}"
        return phone_str
    
    def get_profile_picture_url(self):
        """Return profile picture URL or default"""
        if self.userpic:
            return self.userpic.url
        return '/static/images/default-avatar.png'  # Make sure to add a default image


# Signal to create UserRegisteration when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserRegisteration when a new User is created
    This helps prevent AttributeError when accessing user.userregisteration
    """
    if created:
        # Only create if it doesn't exist (prevents duplicate creation)
        UserRegisteration.objects.get_or_create(
            user=instance,
            defaults={
                'phone': 0,  # Placeholder, should be updated by user
                'door_no': '',
                'street': '',
                'landmark': '',
                'city': '',
                'state': '',
                'pincode': '',
            }
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save UserRegisteration when User is saved
    """
    # Try to save if it exists, create if it doesn't
    try:
        instance.userregisteration.save()
    except UserRegisteration.DoesNotExist:
        UserRegisteration.objects.create(
            user=instance,
            phone=0,
            door_no='',
            street='',
            landmark='',
            city='',
            state='',
            pincode=''
        )