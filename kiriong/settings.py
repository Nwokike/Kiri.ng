"""
Django settings for kiriong project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
# Pull the secret key from the .env file
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# --- Application Definitions ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    # Our apps
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'marketplace.apps.MarketplaceConfig',
    'academy.apps.AcademyConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Middleware for handling language preference.
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kiriong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kiriong.wsgi.application'

# --- Database ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization (i18n) ---
# Default language code.
LANGUAGE_CODE = 'en'
# Supported languages for the site.
LANGUAGES = [
    ('en', _('English')),
    ('ha', _('Hausa')),
    ('ig', _('Igbo')),
    ('yo', _('Yoruba')),
]
# Timezone for the project (Lagos, Nigeria).
TIME_ZONE = 'Africa/Lagos'
# Enable Django's translation system.
USE_I18N = True
# Enable timezone-aware datetimes.
USE_TZ = True

# --- Static files (CSS, JavaScript, Images) ---
# URL to use when referring to static files.
STATIC_URL = 'static/'
# **IMPORTANT**: This tells Django to look for a 'static' folder in the project's root directory.
STATICFILES_DIRS = [BASE_DIR / 'static']

# --- Media files (User-uploaded content) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- General Settings ---
# Default primary key field type.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Where to redirect users after a successful login.
LOGIN_REDIRECT_URL = 'core:home'
