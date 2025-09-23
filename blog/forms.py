from django import forms
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # --- Add header_image ---
        fields = ['title', 'header_image', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'header_image': forms.FileInput(attrs={'class': 'form-control mb-3'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
        }
        help_texts = {
            'title': _('Choose a catchy and descriptive title for your story or tutorial.'),
        }

# --- This is the new form for blog comments ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Write your comment here...')}),
        }
        labels = {'body': ''}