from django.urls import path
from marketplace.views import ServiceListView
from . import views

app_name = 'core'

urlpatterns = [
    path('', ServiceListView.as_view(), name='home'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact-support/', views.contact_support, name='contact-support'),
    path('ai-support/', views.ai_support, name='ai-support'),
    path('api/ai-chat/', views.ai_chat, name='ai-chat'),
    path('api/ai-quick-help/', views.ai_quick_help, name='ai-quick-help'),
]