from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django.core.exceptions import ValidationError

# --- This is our reusable size validator ---
def validate_image_size(value):
    limit = 2 * 1024 * 1024  # 2MB
    if value and value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MB.'))

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required.')
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email",)

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'class': 'form-control'}), 
        validators=[validate_image_size], # <-- Add the validator
        help_text=_("Max size 2MB.") # <-- Add help text
    )
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'phone_number', 'street_address', 'city', 'state', 'business_page_url']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'business_page_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g., https://instagram.com/your-business'}),
        }