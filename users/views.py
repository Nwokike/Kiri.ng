from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile
from django.http import JsonResponse
import json
import requests # <-- THIS IS THE FIX

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

@login_required
def profile_edit_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)

            # --- THE FIX: Read from the hidden fields ---
            if profile.location_verified:
                # Get the verified city/state from the hidden POST data
                updated_profile.city = request.POST.get('verified_city', profile.verified_city)
                updated_profile.state = request.POST.get('verified_state', profile.verified_state)
            
            # Automated verification logic
            if updated_profile.location_verified and updated_profile.business_page_url:
                if not updated_profile.is_verified_artisan:
                    updated_profile.is_verified_artisan = True
                    messages.success(request, 'Congratulations! You are now a Kiri.ng Verified Artisan.')
                else:
                    messages.success(request, 'Your profile has been updated successfully!')
            else:
                 messages.info(request, 'Your profile has been updated. Complete all verification steps to become an artisan.')

            updated_profile.save()
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