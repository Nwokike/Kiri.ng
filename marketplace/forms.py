from django import forms
from .models import Service, Booking, ServiceImage
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# --- NEW: File Size Validator ---
def validate_file_size(value):
    # Limit upload size to 2MB
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MB.'))

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ServiceForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[validate_file_size]
    )
    additional_images = MultipleFileField(
        required=False,
        help_text=_('You can upload multiple images (max 2MB each)')
    )
    
    class Meta:
        model = Service
        fields = ['category', 'title', 'description', 'price', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'customer_phone', 'message']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number (Optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message to the artisan...'}),
        }