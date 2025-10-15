from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from decouple import config  # Added for secure .env loading

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- API Keys and Secrets ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
YOUTUBE_API_KEY = config('YOUTUBE_API_KEY', default='')
BREVO_API_KEY = config('BREVO_API_KEY', default='')
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

# Google Analytics and AdSense
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')
GOOGLE_ADSENSE_CLIENT_ID = config('GOOGLE_ADSENSE_CLIENT_ID', default='')

# --- Core Django Settings ---
# In development (Replit), DEBUG should be True
# Only set to False in production by checking for production environment indicator
IS_PRODUCTION = config('IS_PRODUCTION', default=False, cast=bool)
DEBUG = not IS_PRODUCTION
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=lambda v: [s.strip() for s in v.split(',')])

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = []
if 'REPLIT_DEV_DOMAIN' in os.environ:
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ['REPLIT_DEV_DOMAIN']}")
if not DEBUG:
    CSRF_TRUSTED_ORIGINS.extend([
        'https://kiri.ng',
        'https://www.kiri.ng',
    ])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Third-party apps
    'rest_framework',
    'django_ckeditor_5',
    'django_recaptcha',
    'anymail',
    'cloudinary_storage',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Local apps
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'marketplace.apps.MarketplaceConfig',
    'academy.apps.AcademyConfig',
    'blog.apps.BlogConfig',
    'notifications.apps.NotificationsConfig',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --- Allauth / Google OAuth ---
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': config('GOOGLE_OAUTH_CLIENT_ID', default=''),
            'secret': config('GOOGLE_OAUTH_CLIENT_SECRET', default=''),
        },
    },
}

ACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

LOGIN_REDIRECT_URL = 'core:home'
ACCOUNT_LOGOUT_REDIRECT_URL = 'core:home'
LOGIN_URL = 'login'

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'kiriong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'kiriong.wsgi.application'

# --- Database ---
if 'DATABASE_URL' in os.environ:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                default=config('DATABASE_URL'),
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except Exception:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --- CKEditor ---
CKEDITOR_5_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CKEDITOR_5_FILE_UPLOAD_PERMISSION = 'authenticated'  # Allow authenticated users to upload

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', '|',
                    'undo', 'redo'],
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph'},
                {'model': 'heading1', 'title': 'Heading 1'},
                {'model': 'heading2', 'title': 'Heading 2'},
                {'model': 'heading3', 'title': 'Heading 3'},
            ]
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft',
                'imageStyle:alignCenter', 
                'imageStyle:alignRight'
            ],
            'styles': [
                'full',
                'alignLeft',
                'alignCenter',
                'alignRight'
            ]
        },
    },
}

# --- Password Validators ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Localization ---
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('ha', _('Hausa')),
    ('ig', _('Igbo')),
    ('yo', _('Yoruba')),
]
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / 'media'

# --- Email (Brevo) ---
EMAIL_BACKEND = 'anymail.backends.brevo.EmailBackend'
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='nwokikeonyeka@gmail.com')
ANYMAIL = {"BREVO_API_KEY": BREVO_API_KEY}

# --- Cloudinary ---
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

# --- Misc Defaults ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

# --- Production Security ---
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
