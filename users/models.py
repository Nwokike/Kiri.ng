from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified_artisan = models.BooleanField(default=False)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    # User-editable street address
    street_address = models.CharField(max_length=255, blank=True)
    
    # These are now the main, displayable fields
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    # These are temporary holders from the GPS check
    verified_city = models.CharField(max_length=100, blank=True, null=True)
    verified_state = models.CharField(max_length=100, blank=True, null=True)
    
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    business_page_url = models.URLField(max_length=500, blank=True, null=True, help_text=_("Your Instagram, Facebook, or WhatsApp Business link."))
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    
    location_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def successful_referrals_count(self):
        return self.user.referrals.count()

class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('whatsapp', 'WhatsApp Business'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField(max_length=500)
    is_primary = models.BooleanField(default=False, help_text=_("Primary link used for verification"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'platform']
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.get_platform_display()}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            SocialMediaLink.objects.filter(profile=self.profile, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=200, help_text=_("Certificate name (e.g., Plumbing Certification, Electrical Safety)"))
    issuing_organization = models.CharField(max_length=200, help_text=_("Who issued this certificate"))
    issue_date = models.DateField(help_text=_("When was this certificate issued"))
    expiry_date = models.DateField(blank=True, null=True, help_text=_("Leave blank if it doesn't expire"))
    certificate_image = models.ImageField(upload_to='certificates/', help_text=_("Upload certificate image"))
    description = models.TextField(blank=True, help_text=_("Additional details about this certification"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.title}"
    
    @property
    def is_expired(self):
        if self.expiry_date:
            from datetime.date import today
            return self.expiry_date < today()
        return False