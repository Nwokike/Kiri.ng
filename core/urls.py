from django.urls import path
from marketplace.views import ServiceListView  # <-- Import the correct view
from . import views

app_name = 'core'

urlpatterns = [
    path('', ServiceListView.as_view(), name='home'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
]