from django import forms
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_image_size(value):
    limit = 2 * 1024 * 1024  # 2MB
    if value and value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MB.'))

class PostForm(forms.ModelForm):
    header_image = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'}),
        validators=[validate_image_size],
        help_text=_("Optional. Max size 2MB.")
    )
    class Meta:
        model = Post
        fields = ['title', 'category', 'meta_description', 'header_image', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'category': forms.Select(attrs={'class': 'form-select mb-3'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 2, 'maxlength': 160, 'placeholder': _('Brief description for search engines (max 160 characters)')}),
        }
        help_texts = {
            'title': _('Choose a catchy and descriptive title for your story or tutorial.'),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Write your comment here...')}),
        }
        labels = {'body': ''}