from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# This is a signal: it creates a Profile automatically when a User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
