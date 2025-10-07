from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'core/home.html', {'title': 'Kiri.ng – Empowering Artisans'})

def terms(request):
    return render(request, 'core/terms.html', {'title': 'Terms and Conditions'})

def privacy(request):
    return render(request, 'core/privacy.html', {'title': 'Privacy Policy'})

@require_POST
def contact_support(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    
    try:
        send_mail(
            subject=f'Support Request from {name}',
            message=f'From: {name} ({email})\n\nMessage:\n{message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        messages.success(request, 'Your message has been sent successfully! We\'ll get back to you soon.')
    except Exception as e:
        messages.error(request, 'There was an error sending your message. Please try again later.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))