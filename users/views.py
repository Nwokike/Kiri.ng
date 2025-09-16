from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .forms import SignupForm, ProfileUpdateForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _(f'Account created for {username}! You can now log in.'))
            return redirect('users:login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, _('Your ID has been uploaded and is awaiting verification.'))
            return redirect('users:profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)