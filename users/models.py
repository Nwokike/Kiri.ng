from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified_artisan = models.BooleanField(default=False)
    
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