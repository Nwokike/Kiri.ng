from django import forms
from django.utils.translation import gettext_lazy as _

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

class GoalForm(forms.Form):
    goal = forms.CharField(
        label=_("What is your primary goal?"),
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text=_("Be as specific as you can.")
    )
    location = forms.ChoiceField(
        label=_("Which state are you based in?"),
        choices=NIGERIAN_STATES,
        help_text=_("This helps the AI give you localized advice.")
    )