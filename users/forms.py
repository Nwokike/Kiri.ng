from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True, label=_("I am a..."))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Save the profile with the selected role
            user.profile.role = self.cleaned_data['role']
            user.profile.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('id_photo',) # We only want the user to be able to update their ID photo