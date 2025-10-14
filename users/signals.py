from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.signals import pre_social_login
from .models import Profile
from notifications.models import Notification
from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create profile for new users"""
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_social_login)
def capture_referral_on_social_login(sender, request, sociallogin, **kwargs):
    """Capture referral username when user signs up via Google OAuth"""
    referral_code = request.session.get('referral_code')  # Note: session key kept for backward compatibility
    
    if referral_code and sociallogin.is_existing:
        return
    
    if referral_code:
        try:
            # Try to find referrer by username (new system) or referral_code (legacy)
            try:
                referrer_user = User.objects.get(username=referral_code)
            except User.DoesNotExist:
                referrer_profile = Profile.objects.get(referral_code=referral_code)
                referrer_user = referrer_profile.user
            
            if not sociallogin.is_existing:
                user = sociallogin.user
                if user.pk:
                    profile, created = Profile.objects.get_or_create(user=user)
                    if not profile.referred_by:
                        profile.referred_by = referrer_user
                        profile.save()
                        
                        Notification.objects.create(
                            recipient=referrer_user,
                            message=_(f"Congratulations! A new user signed up using your referral link.")
                        )
        except (User.DoesNotExist, Profile.DoesNotExist):
            pass
