from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address', 'autofocus': True})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password. Note that both fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }
    
    def clean_username(self):
        email = self.cleaned_data.get('username')
        if email:
            email = email.lower()
            try:
                user = User.objects.get(email__iexact=email)
                return user.username
            except User.DoesNotExist:
                pass
        return email
