from django import forms
from .models import Post
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
        }
        help_texts = {
            'title': _('Choose a catchy and descriptive title for your story or tutorial.'),
            'body': _('Write your content here. You can share a success story, a tutorial, or advice for other artisans. Your post will be reviewed before publishing.'),
        }