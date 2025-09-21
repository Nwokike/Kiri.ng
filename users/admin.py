from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    """
    # This tells the admin what columns to show in the list of profiles.
    list_display = ('user', 'is_verified_artisan', 'state', 'city')
    
    # This adds a filter sidebar to easily find users.
    list_filter = ('is_verified_artisan', 'state')
    
    # This adds a search bar.
    search_fields = ('user__username', 'state', 'city')