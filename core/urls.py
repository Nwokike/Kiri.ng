from django.urls import path
from marketplace.views import ServiceListView  # <-- Import the correct view
from . import views

app_name = 'core'

urlpatterns = [
    # --- THIS IS THE FIX: The homepage is now the service list ---
    path('', ServiceListView.as_view(), name='home'),
]