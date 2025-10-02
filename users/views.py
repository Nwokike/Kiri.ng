from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile, User, SocialMediaLink
from django.http import JsonResponse
import json
import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import urllib.parse
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from notifications.models import Notification  # Added import


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            referral_code = form.cleaned_data.get('referral_code')
            referred_by_user = None

            if referral_code:
                try:
                    referred_by_user = User.objects.get(username__iexact=referral_code)
                    Notification.objects.create(
                        recipient=referred_by_user,
                        message=_(f"Congratulations! {user.username} signed up using your referral code.")
                    )
                except User.DoesNotExist:
                    pass

            profile = Profile.objects.create(user=user, referred_by=referred_by_user)
            
            verification_url = request.build_absolute_uri(
                f'/users/verify-email/{profile.email_verification_token}/'
            )
            context = {
                'user': user,
                'verification_url': verification_url
            }
            html_message = render_to_string('registration/email_verification.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                _('Verify Your Email - Kiri.ng'),
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )
            
            login(request, user)
            messages.info(request, _('Please check your email to verify your account.'))
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile_detail.html', {'profile': profile})


def send_welcome_artisan_email(user, profile):
    google_link = profile.google_maps_link or "#"
    context = {'user': user, 'google_link': google_link}
    html_message = render_to_string('registration/welcome_artisan_email.html', context)
    plain_message = strip_tags(html_message)
    print(f"--- SENDING WELCOME ARTISAN EMAIL to {user.email} ---")
    send_mail(
        _('Welcome to Kiri.ng!'),
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )


@login_required
def profile_edit_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    was_verified_before = profile.is_verified_artisan

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)

            if updated_profile.location_verified and updated_profile.business_page_url:
                updated_profile.is_verified_artisan = True
                if not updated_profile.google_maps_link:
                    query = f"{updated_profile.street_address}, {updated_profile.city}, {updated_profile.state}, Nigeria"
                    encoded_query = urllib.parse.quote_plus(query)
                    updated_profile.google_maps_link = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

            updated_profile.save()

            # Handle multiple social media links
            social_links_count = int(request.POST.get('social_links_count', 0))
            removed_links = request.POST.get('removed_social_links', '')
            
            # Remove deleted links
            if removed_links:
                link_ids = [int(lid) for lid in removed_links.split(',') if lid]
                SocialMediaLink.objects.filter(id__in=link_ids, profile=profile).delete()
            
            # Update or create social links
            for i in range(social_links_count):
                platform = request.POST.get(f'social_platform_{i}')
                url = request.POST.get(f'social_url_{i}')
                is_primary = request.POST.get(f'social_primary_{i}') == 'on'
                link_id = request.POST.get(f'social_id_{i}')
                
                if platform and url:
                    if link_id:
                        # Update existing link
                        try:
                            link = SocialMediaLink.objects.get(id=int(link_id), profile=profile)
                            link.platform = platform
                            link.url = url
                            link.is_primary = is_primary
                            link.save()
                        except SocialMediaLink.DoesNotExist:
                            pass
                    else:
                        # Create new link
                        SocialMediaLink.objects.create(
                            profile=profile,
                            platform=platform,
                            url=url,
                            is_primary=is_primary
                        )

            # --- CREATE NOTIFICATION FOR PROFILE UPDATE ---
            Notification.objects.create(
                recipient=request.user,
                message=_("Your profile was updated successfully.")
            )

            if updated_profile.is_verified_artisan and not was_verified_before:
                messages.success(request, _('Congratulations! You are now a Kiri.ng Verified Artisan.'))
                send_welcome_artisan_email(request.user, updated_profile)
            else:
                messages.success(request, _('Your profile has been updated successfully!'))

            return redirect('users:profile-detail')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def verify_location_view(request):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=request.user)
        try:
            data = json.loads(request.body)
            latitude, longitude = data.get('latitude'), data.get('longitude')
            if latitude is not None and longitude is not None:
                url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18"
                response = requests.get(url, headers={'User-Agent': 'Kiri.ng/1.0'})
                response.raise_for_status()
                address_data = response.json().get('address', {})

                city = (
                    address_data.get('city')
                    or address_data.get('village')
                    or address_data.get('county')
                    or address_data.get('town')
                    or address_data.get('locality')
                    or address_data.get('municipality')
                    or address_data.get('district')
                    or address_data.get('suburb')
                    or ''
                )
                state = (
                    address_data.get('state')
                    or address_data.get('region')
                    or address_data.get('state_district')
                    or ''
                )

                profile.city, profile.state = city, state
                profile.verified_city, profile.verified_state = city, state
                profile.location_verified = True
                profile.save()

                return JsonResponse({'status': 'success', 'city': city, 'state': state})
            else:
                return JsonResponse({'status': 'error', 'message': 'Coordinates missing.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


class ArtisanStorefrontView(generic.DetailView):
    model = User
    template_name = 'users/artisan_storefront.html'
    context_object_name = 'artisan'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from academy.models import LearningPathway
        from django.db.models import Count, Q
        artisan = self.get_object()
        
        pathways = LearningPathway.objects.filter(
            user=artisan
        ).prefetch_related('modules').annotate(
            total_modules=Count('modules'),
            incomplete_modules=Count('modules', filter=Q(modules__is_completed=False))
        )
        
        completed_pathways = [
            p for p in pathways 
            if p.total_modules > 0 and p.incomplete_modules == 0
        ]
        context['completed_pathways'] = completed_pathways
        return context


def custom_logout(request):
    logout(request)
    messages.success(request, _("You have been successfully logged out."))
    return redirect('core:home')


def verify_email(request, token):
    try:
        profile = Profile.objects.get(email_verification_token=token)
        if not profile.email_verified:
            profile.email_verified = True
            profile.save()
            messages.success(request, _("Your email has been verified successfully!"))
        else:
            messages.info(request, _("Your email is already verified."))
        return redirect('users:profile-detail')
    except Profile.DoesNotExist:
        messages.error(request, _("Invalid verification link."))
        return redirect('core:home')


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, _("Your account has been permanently deleted."))
        return redirect('core:home')
    return render(request, 'users/delete_account_confirm.html')
