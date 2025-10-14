from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ai_customer_service import AICustomerService

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


def ai_support(request):
    """AI customer support chat interface"""
    return render(request, 'core/ai_support.html', {'title': 'AI Customer Support'})


@require_POST
def ai_chat(request):
    """Handle AI chat messages"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        ai_service = AICustomerService()
        response = ai_service.get_chat_response(
            user_message, 
            user=request.user if request.user.is_authenticated else None,
            conversation_history=conversation_history
        )
        
        return JsonResponse({'response': response})
    except Exception as e:
        return JsonResponse({'response': f'Sorry, I encountered an error: {str(e)}'}, status=500)


@require_POST  
def ai_quick_help(request):
    """Handle quick help requests"""
    try:
        data = json.loads(request.body)
        task_type = data.get('task_type', '')
        
        ai_service = AICustomerService()
        response = ai_service.help_with_task(
            task_type,
            user=request.user if request.user.is_authenticated else None
        )
        
        return JsonResponse({'response': response})
    except Exception as e:
        return JsonResponse({'response': f'Error: {str(e)}'}, status=500)


def indexnow_key(request, key):
    """Serve IndexNow key verification file"""
    from .indexnow import get_indexnow_key
    from django.http import HttpResponse
    
    if key == get_indexnow_key():
        return HttpResponse(key, content_type='text/plain')
    return HttpResponse(status=404)