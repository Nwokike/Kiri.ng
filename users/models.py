from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid # Make sure this import is here

class Profile(models.Model):
    ROLE_CHOICES = (
        ('entrepreneur', _('Entrepreneur')),
        ('buyer', _('Buyer')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    role = models.CharField(_("Role"), max_length=20, choices=ROLE_CHOICES, default='buyer')
    id_photo = models.ImageField(_("ID Photo"), upload_to='ids/', blank=True, null=True, help_text=_("Upload a photo of your NIN slip, Passport, or Driver's License."))
    verified = models.BooleanField(_("Verified"), default=False)
    match_notes = models.TextField(_("Admin Verification Notes"), blank=True, help_text=_("Notes on why the user was approved or rejected."))
    
    # --- THESE FIELDS WERE MISSING ---
    referral_code = models.CharField(_("Referral Code"), max_length=12, unique=True, blank=True)
    credits = models.PositiveIntegerField(_("Credits"), default=0)
    
    # --- THESE FIELDS WERE ADDED CORRECTLY ---
    entrepreneur_level = models.PositiveIntegerField(_("Entrepreneur Level"), default=1)
    experience_points = models.PositiveIntegerField(_("Experience Points (XP)"), default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        # Generate and save a unique referral code
        if not profile.referral_code:
            profile.referral_code = str(uuid.uuid4())[:8].upper()
            profile.save()

