from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class CustomLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
