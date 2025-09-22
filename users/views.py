from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile
from django.http import JsonResponse
import json
import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import urllib.parse
from django.views import generic
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def signup(request):
    # ... (no changes) ...
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_view(request):
    # ... (no changes) ...
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile_detail.html', {'profile': profile})

def send_welcome_artisan_email(user, profile):
    # ... (no changes) ...
    google_link = profile.google_maps_link or "#"
    context = {'user': user, 'google_link': google_link}
    html_message = render_to_string('registration/welcome_artisan_email.html', context)
    plain_message = strip_tags(html_message)
    print(f"--- SENDING WELCOME ARTISAN EMAIL to {user.email} ---")
    send_mail(_('Welcome to Kiri.ng!'), plain_message, 'noreply@kiri.ng', [user.email], html_message=html_message)

@login_required
def profile_edit_view(request):
    # ... (no changes) ...
    profile = get_object_or_404(Profile, user=request.user)
    was_verified_before = profile.is_verified_artisan
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)
            # The city/state are now updated by the verify_location_view, so we just check the flag
            if updated_profile.location_verified and updated_profile.business_page_url:
                updated_profile.is_verified_artisan = True
                if not updated_profile.google_maps_link:
                    query = f"{updated_profile.street_address}, {updated_profile.city}, {updated_profile.state}, Nigeria"
                    encoded_query = urllib.parse.quote_plus(query)
                    updated_profile.google_maps_link = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
            updated_profile.save()
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
            # --- THIS IS THE FIX: We are back to using browser GPS ---
            data = json.loads(request.body)
            latitude, longitude = data.get('latitude'), data.get('longitude')
            if latitude is not None and longitude is not None:
                url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18"
                response = requests.get(url, headers={'User-Agent': 'Kiri.ng/1.0'})
                response.raise_for_status() # Check for errors
                address_data = response.json().get('address', {})
                
                # We save the verified data to both sets of fields
                city = address_data.get('city', address_data.get('town', address_data.get('village', '')))
                state = address_data.get('state', '')
                profile.city, profile.state = city, state
                profile.verified_city, profile.verified_state = city, state
                profile.location_verified = True
                profile.save()
                
                return JsonResponse({'status': 'success', 'city': city, 'state': state})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

# ... ArtisanStorefrontView and custom_logout remain unchanged ...
class ArtisanStorefrontView(generic.DetailView):
    model = User
    template_name = 'users/artisan_storefront.html'
    context_object_name = 'artisan'
    slug_field = 'username'
    slug_url_kwarg = 'username'

def custom_logout(request):
    logout(request)
    messages.success(request, _("You have been successfully logged out."))
    return redirect('core:home')