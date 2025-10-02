from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile, SocialMediaLink
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

# --- This is our reusable size validator ---
def validate_image_size(value):
    limit = 2 * 1024 * 1024  # 2MB
    if value and value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MB.'))

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required.')
    referral_code = forms.CharField(max_length=150, required=False, label=_('Referral Code (Optional)'))
    accept_terms = forms.BooleanField(
        required=True,
        label='',
        error_messages={'required': _('You must accept the terms and conditions to sign up.')}
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email",)

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