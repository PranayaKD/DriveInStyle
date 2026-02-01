# btmapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserRegisteration


class UserRegisterationInline(admin.StackedInline):
    """
    Inline admin for UserRegisteration to show in User admin
    """
    model = UserRegisteration
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fk_name = 'user'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('phone',)
        }),
        ('Address', {
            'fields': ('door_no', 'street', 'landmark', 'city', 'state', 'pincode')
        }),
        ('Profile Picture', {
            'fields': ('userpic',)
        }),
    )


class UserAdmin(BaseUserAdmin):
    """
    Extended User admin with UserRegisteration inline
    """
    inlines = (UserRegisterationInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')


@admin.register(UserRegisteration)
class UserRegisterationAdmin(admin.ModelAdmin):
    """
    Admin interface for UserRegisteration model
    """
    list_display = ('user', 'phone', 'city', 'state', 'created_at')
    list_filter = ('state', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city', 'pincode')
    readonly_fields = ('created_at', 'updated_at', 'full_address')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone',)
        }),
        ('Address', {
            'fields': ('door_no', 'street', 'landmark', 'city', 'state', 'pincode', 'full_address')
        }),
        ('Profile Picture', {
            'fields': ('userpic',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queries by selecting related user"""
        queryset = super().get_queryset(request)
        return queryset.select_related('user')


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)