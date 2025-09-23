from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _
from .models import Comment 

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

# --- Restoring your superior GoalForm ---
class GoalForm(forms.Form):
    goal = forms.CharField(
        label=_("What is your primary business goal?"),
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        help_text=_("e.g., 'Master social media marketing for my tailoring business'")
    )
    location = forms.ChoiceField(
        label=_("Which state are you based in?"),
        choices=NIGERIAN_STATES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text=_("This helps the AI give you localized advice.")
    )

# --- This is our simple and correct CommentForm ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment or ask a question...'}),
        }
        labels = {
            'body': ''  # No label for the comment box
        }