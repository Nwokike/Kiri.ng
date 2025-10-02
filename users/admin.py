from django.contrib import admin
from .models import Profile, SocialMediaLink, Certificate

class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 2
    fields = ('platform', 'url', 'is_primary')

class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1
    fields = ('title', 'issuing_organization', 'issue_date', 'expiry_date', 'certificate_image')

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
    
    inlines = [SocialMediaLinkInline, CertificateInline]

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('profile', 'platform', 'url', 'is_primary')
    list_filter = ('platform', 'is_primary')
    search_fields = ('profile__user__username', 'url')