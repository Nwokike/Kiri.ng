from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import Profile, SocialMediaLink


# --- This is our reusable size validator ---
def validate_image_size(value):
    limit = 2 * 1024 * 1024  # 2MB
    if value and value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MB.'))


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required.')
    email = forms.EmailField(
        required=True,
        help_text=_('Required. Enter a valid email address.'),
        error_messages={
            'required': _('Email is required.'),
            'invalid': _('Enter a valid email address.')
        }
    )
    accept_terms = forms.BooleanField(
        required=True,
        label='',
        error_messages={'required': _('You must accept the terms and conditions to sign up.')}
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta(UserCreationForm.Meta):
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            from django.contrib.auth.models import User
            if User.objects.filter(email__iexact=email).exists():
                raise ValidationError(
                    _('An account with this email already exists. Please use a different email or login to your existing account.')
                )
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        from django.contrib.auth.models import User
        import re
        
        email = self.cleaned_data['email']
        base_username = email.split('@')[0]
        base_username = re.sub(r'[^a-zA-Z0-9_]', '', base_username)[:20]
        
        if not base_username:
            first_name = self.cleaned_data.get('first_name', '').lower()
            last_name = self.cleaned_data.get('last_name', '').lower()
            base_username = f"{first_name}{last_name}"
            base_username = re.sub(r'[^a-zA-Z0-9_]', '', base_username)[:20]
        
        if not base_username:
            base_username = 'user'
        
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user.username = username
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'class': 'form-control'}), 
        validators=[validate_image_size],
        help_text=_("Max size 2MB.")
    )
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': False}))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'phone_number', 'street_address', 'city', 'state']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SocialMediaLinkForm(forms.ModelForm):
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'is_primary']
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'url': _('Please include https:// at the beginning (e.g., https://instagram.com/yourprofile)'),
        }


# 🚀 ADDED THIS NEW FORM
class AccountDeleteForm(forms.Form):
    """
    A simple form to confirm account deletion by requiring the user's password.
    """
    password = forms.CharField(
        label=_("Confirm Password"),
        strip=False, # Important for passwords not to have whitespace stripped
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )
