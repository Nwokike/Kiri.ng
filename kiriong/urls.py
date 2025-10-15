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

    # Custom CKEditor upload endpoint
    path('ckeditor5/image_upload/', custom_upload_file, name='ckeditor5_upload'),
    
    # App URLs
    path('', include('core.urls')),
    path('users/', include('users.urls')), 
    path('marketplace/', include('marketplace.urls')),
    path('academy/', include('academy.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
    path('blog/', include('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    
    path('accounts/', include('allauth.urls')),
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # path('password-reset/', ...),
    # path('password-reset/done/', ...),
    # path('password-reset-confirm/...', ...),
    # path('password-reset-complete/', ...),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
