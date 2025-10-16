from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from users.auth_forms import CustomLoginForm
from blog.upload_views import custom_upload_file
from core.sitemaps import (
    StaticViewSitemap,
    BlogPostSitemap,
    ServiceSitemap,
    ArtisanProfileSitemap,
    LearningPathwaySitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogPostSitemap,
    'services': ServiceSitemap,
    'artisans': ArtisanProfileSitemap,
    'pathways': LearningPathwaySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/image_upload/', custom_upload_file, name='ckeditor5_upload'),
    
    # App URLs
    path('', include('core.urls')),
    path('users/', include('users.urls')), 
    path('marketplace/', include('marketplace.urls')),
    path('academy/', include('academy.urls')),
    # Your custom login view remains unchanged
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
    path('blog/', include('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    
    # Allauth now handles ALL account management correctly and finds all your styled templates.
    path('accounts/', include('allauth.urls')),
    
    # SEO URL
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
