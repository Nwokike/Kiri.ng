from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.auth_forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('core.urls')),
    path('users/', include('users.urls')), 
    path('marketplace/', include('marketplace.urls')),
    path('academy/', include('academy.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
    path('blog/', include('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
