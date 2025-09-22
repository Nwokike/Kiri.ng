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
from django.utils.translation import gettext_lazy as _ # <-- THIS IS THE FIX

def signup(request):
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
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile_detail.html', {'profile': profile})

def send_welcome_artisan_email(user, profile):
    params = {
        'business_name': user.get_full_name() or user.username,
        'address_line_1': profile.street_address,
        'address_line_2': f"{profile.city}, {profile.state}",
        'phone_number': profile.phone_number
    }
    encoded_params = urllib.parse.urlencode(params)
    google_link = f"https://www.google.com/business/add?{encoded_params}"

    context = {
        'user': user,
        'google_link': google_link
    }
    html_message = render_to_string('registration/welcome_artisan_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        _('Welcome to Kiri.ng! Your Next Step Awaits.'),
        plain_message,
        'noreply@kiri.ng',
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
    print(f"Welcome email sent to {user.email}")


@login_required
def profile_edit_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    was_verified_before = profile.is_verified_artisan

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)

            if profile.location_verified:
                updated_profile.city = request.POST.get('verified_city', profile.verified_city)
                updated_profile.state = request.POST.get('verified_state', profile.verified_state)
            
            if updated_profile.location_verified and updated_profile.business_page_url:
                updated_profile.is_verified_artisan = True
            
            updated_profile.save()

            if updated_profile.is_verified_artisan and not was_verified_before:
                messages.success(request, _('Congratulations! You are now a Kiri.ng Verified Artisan. Check your email for the next step!'))
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
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is not None and longitude is not None:
                url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
                response = requests.get(url, headers={'User-Agent': 'Kiri.ng/1.0'})
                address_data = response.json().get('address', {})
                
                street = address_data.get('road', '')
                city = address_data.get('city', address_data.get('town', ''))
                state = address_data.get('state', '')

                profile.verified_street_address = street
                profile.verified_city = city
                profile.verified_state = state
                profile.location_verified = True
                profile.save()
                
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Location received.',
                    'address': f"{street}, {city}, {state}"
                })
        except Exception as e:
            print(f"Error in location verification: {e}")
            return JsonResponse({'status': 'error', 'message': 'Could not process location.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


class ArtisanStorefrontView(generic.DetailView):
    model = User
    template_name = 'users/artisan_storefront.html'
    context_object_name = 'artisan'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artisan_user = self.get_object()
        return context

def custom_logout(request):
    logout(request)
    messages.success(request, _("You have been successfully logged out."))
    return redirect('core:home')