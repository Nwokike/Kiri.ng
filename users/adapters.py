from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import User
from .models import Profile
from notifications.models import Notification
from django.utils.translation import gettext_lazy as _


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Handle referral code capture and account linking for social logins"""
        # If user exists, try to connect the account
        if sociallogin.is_existing:
            return

        # Check if email exists
        if sociallogin.user.email:
            try:
                existing_user = User.objects.get(email=sociallogin.user.email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        """Save social login user and handle referral code"""
        user = super().save_user(request, sociallogin, form)
        
        referral_code = request.session.get('referral_code')
        if referral_code:
            try:
                # Try to find referrer by username (new system) or referral_code (legacy)
                try:
                    referrer_user = User.objects.get(username=referral_code)
                except User.DoesNotExist:
                    referrer_profile = Profile.objects.get(referral_code=referral_code)
                    referrer_user = referrer_profile.user
                
                profile, created = Profile.objects.get_or_create(user=user)
                
                if not profile.referred_by:
                    profile.referred_by = referrer_user
                    profile.save()
                    
                    Notification.objects.create(
                        recipient=referrer_user,
                        message=_(f"Congratulations! {user.username or user.email} signed up using your referral link.")
                    )
                    
                del request.session['referral_code']
            except (User.DoesNotExist, Profile.DoesNotExist):
                pass
        
        return user


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_safe_url(self, url):
        """Override to allow custom redirects"""
        return super().is_safe_url(url)
