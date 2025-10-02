from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _
from .models import Comment 
from marketplace.models import Category

# --- Restoring the full list of states from your version ---
NIGERIAN_STATES = [
    ('', _('Select your state...')), ('Abia', 'Abia'), ('Adamawa', 'Adamawa'), ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'),
    ('Cross River', 'Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'), ('FCT', 'Federal Capital Territory'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara'),
]

# --- Predefined business goals for artisans ---
BUSINESS_GOALS = [
    ('', _('Select your business goal...')),
    ('start_small_business', _('Start a small business from scratch')),
    ('grow_existing_business', _('Grow my existing business')),
    ('learn_marketing', _('Learn marketing and customer acquisition')),
    ('improve_service_quality', _('Improve my service quality and skills')),
    ('manage_finances', _('Manage business finances and pricing')),
    ('build_online_presence', _('Build an online presence for my business')),
    ('customer_service', _('Improve customer service and retention')),
    ('scale_operations', _('Scale my operations and hire helpers')),
]

# --- Updated GoalForm with predefined dropdown options only ---
class GoalForm(forms.Form):
    category = forms.ModelChoiceField(
        label=_("What skill or trade do you want to master?"),
        queryset=Category.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text=_("Select the artisan skill you want to learn to start your business")
    )
    goal = forms.ChoiceField(
        label=_("What is your main business goal?"),
        choices=BUSINESS_GOALS,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text=_("This will help us create a personalized pathway for you to become a successful artisan")
    )
    location = forms.ChoiceField(
        label=_("Which state are you based in?"),
        choices=NIGERIAN_STATES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text=_("We'll provide localized advice for your area")
    )

# --- Comment Form ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment or ask a question...'}),
        }
        labels = {
            'body': ''
        }

# --- Question Form for AI Instructor ---
class QuestionForm(forms.Form):
    question = forms.CharField(
        label=_("Ask the AI Instructor"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ask a question about this module...'}),
        help_text=_("Get instant AI-powered answers to your questions about this module")
    )