from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- THIS IS THE FIX ---
    # This single line includes all of Django's built-in auth URLs
    # like login/, logout/, password_reset/, etc.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Our custom app URLs
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('services/', include('marketplace.urls')),
    path('academy/', include('academy.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)