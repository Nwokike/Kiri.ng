from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from users.auth_forms import CustomLoginForm
from blog.upload_views import custom_upload_file
from core.sitemaps import (
    StaticViewSitemap, BlogPostSitemap, ServiceSitemap,
    ArtisanProfileSitemap, LearningPathwaySitemap
)
# 🚀 IMPORT ALLAUTH'S VIEWS SO WE CAN CUSTOMIZE THEM 🚀
from allauth.account import views as allauth_views

sitemaps = {
    'static': StaticViewSitemap, 'blog': BlogPostSitemap, 'services': ServiceSitemap,
    'artisans': ArtisanProfileSitemap, 'pathways': LearningPathwaySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/image_upload/', custom_upload_file, name='ckeditor5_upload'),
    
    # App URLs
    path('', include('core.urls')),
    path('users/', include('users.urls')), 
    path('marketplace/', include('marketplace.urls')),
    path('academy/', include('academy.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
    path('blog/', include('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    
    # 🚀 FIX: EXPLICITLY DEFINE PASSWORD RESET URLS TO USE YOUR STYLED TEMPLATES 🚀
    # These paths override the default allauth templates and use yours from the /registration/ folder.
    path(
        'accounts/password/reset/', 
        allauth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
            email_template_name='registration/password_reset_email.html'  # This fixes your email styling
        ), 
        name='account_reset_password'
    ),
    path(
        'accounts/password/reset/done/', 
        allauth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='account_password_reset_done'
    ),
    path(
        'accounts/password/reset/key/<uidb36>/<key>/',
        allauth_views.PasswordResetFromKeyView.as_view(template_name='registration/password_reset_confirm.html'),
        name='account_reset_password_from_key'
    ),
    path(
        'accounts/password/reset/key/done/',
        allauth_views.PasswordResetFromKeyDoneView.as_view(template_name='registration/password_reset_complete.html'),
        name='account_reset_password_from_key_done'
    ),

    # Allauth handles all other account management (signup, logout, etc.)
    path('accounts/', include('allauth.urls')),
    
    # SEO URL
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
