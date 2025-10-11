# Kiri.ng - Project Structure

## Project Tree
```
kiriong/                          # Django project root
├── academy/                      # AI-powered learning platform app
│   ├── migrations/              # Database migrations
│   ├── templates/academy/       # Academy-specific templates
│   │   ├── academy_home.html
│   │   ├── certificate.html
│   │   ├── create_pathway.html
│   │   ├── dashboard.html
│   │   ├── pathway_detail.html
│   │   ├── pathway_list.html
│   │   └── public_pathway_detail.html
│   ├── templatetags/           # Custom template tags
│   │   ├── __init__.py
│   │   └── academy_extras.py
│   ├── admin.py
│   ├── ai_services.py          # Gemini AI integration
│   ├── apps.py
│   ├── forms.py
│   ├── models.py               # LearningPathway, PathwayModule, Badge, etc.
│   ├── urls.py
│   └── views.py
│
├── blog/                        # Community blogging app
│   ├── migrations/
│   ├── templates/blog/
│   │   ├── post_detail.html
│   │   ├── post_form.html
│   │   └── post_list.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py               # CKEditor integration
│   ├── models.py              # Post, Comment
│   ├── urls.py
│   └── views.py
│
├── core/                        # Core functionality & base templates
│   ├── migrations/
│   ├── templates/core/
│   │   ├── base.html          # Master base template
│   │   ├── privacy.html
│   │   └── terms.html
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py  # Global context data
│   ├── models.py
│   ├── urls.py
│   └── views.py               # Homepage, support
│
├── marketplace/                 # Services & bookings app
│   ├── migrations/
│   ├── templates/marketplace/
│   │   ├── artisan_dashboard.html
│   │   ├── booking_notification_email.html
│   │   ├── service_confirm_delete.html
│   │   ├── service_detail.html
│   │   ├── service_form.html
│   │   └── service_list.html
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── marketplace_tags.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py              # Category, Service, Booking
│   ├── recommender.py         # Service recommendations
│   ├── urls.py
│   └── views.py
│
├── notifications/               # Real-time notifications app
│   ├── migrations/
│   ├── templates/notifications/
│   │   └── notification_list.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # Notification
│   ├── urls.py
│   └── views.py
│
├── users/                       # User profiles & authentication
│   ├── migrations/
│   ├── templates/users/
│   │   ├── certificates.html
│   │   ├── profile_detail.html
│   │   ├── profile_edit.html
│   │   └── profile.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py              # Profile, Certificate, SocialMediaLink
│   ├── urls.py
│   └── views.py
│
├── kiriong/                     # Django settings & config
│   ├── asgi.py
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py
│
├── static/                      # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   ├── dashboard.js       # Dashboard functionality
│   │   └── theme-toggle.js    # Dark/light mode
│   └── images/
│       ├── logo-dark.png
│       └── logo.png
│
├── staticfiles/                 # Collected static files (production)
│
├── templates/                   # Global templates
│   ├── registration/           # Auth & email templates
│   │   ├── artisan_dashboard.html
│   │   ├── email_verification.html
│   │   ├── login.html
│   │   ├── password_reset_complete.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_email.html
│   │   ├── password_reset.html
│   │   ├── signup.html
│   │   └── welcome_artisan_email.html
│   └── email_base.html         # Email template base
│
├── media/                       # User-uploaded files
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD configuration
│
├── manage.py                    # Django management script
├── build.sh                     # Build script
├── requirements.txt             # Python dependencies
├── .gitignore
├── replit.md                    # Project documentation
├── AUDIT_FINDINGS.md           # Audit report
├── DEPLOYMENT_CHECKLIST.md     # Deployment guide
└── PROJECT_STRUCTURE.md        # This file
```

## Django Apps Overview

### 1. Academy (AI Learning Platform)
- **Models**: LearningPathway, PathwayModule, ModuleVideo, ModuleQuestion, Badge, UserBadge, Comment
- **Features**: AI-generated learning paths using Gemini 2.5 Flash, YouTube integration, badges, certificates
- **Key Files**: `ai_services.py` (Gemini integration), `views.py` (pathway creation)

### 2. Blog (Community Content)
- **Models**: Post, Comment
- **Features**: CKEditor rich text, image uploads via Cloudinary, commenting system
- **Key Files**: `forms.py` (CKEditor config), `views.py` (CRUD operations)

### 3. Core (Base Functionality)
- **Models**: None (shared utilities)
- **Features**: Homepage, support page, base templates, context processors
- **Key Files**: `base.html` (master template), `context_processors.py`

### 4. Marketplace (Services & Bookings)
- **Models**: Category, Service, ServiceImage, Booking
- **Features**: Service listings, multi-image uploads, booking system, recommendations
- **Key Files**: `recommender.py` (ML recommendations), `views.py` (service CRUD)

### 5. Notifications
- **Models**: Notification
- **Features**: Real-time user notifications, read/unread tracking
- **Key Files**: `models.py`, `views.py`

### 6. Users (Profiles & Auth)
- **Models**: Profile, SocialMediaLink, Certificate
- **Features**: Extended user profiles, Google OAuth, referral system, certificates
- **Key Files**: `models.py` (Profile model), `views.py` (auth views)

## Key Technologies
- **Backend**: Django 5.0.6, PostgreSQL (Replit/Neon)
- **Frontend**: Bootstrap 5.3.3, Vanilla JavaScript
- **AI**: Google Gemini 2.5 Flash, YouTube Data API v3
- **Storage**: Cloudinary (images/media)
- **Email**: Brevo (django-anymail)
- **Auth**: Django Allauth, Google OAuth, reCAPTCHA
- **PWA**: Service workers, manifest.json

## Configuration Files
- `kiriong/settings.py`: Main Django settings
- `requirements.txt`: Python dependencies
- `.github/workflows/deploy.yml`: CI/CD pipeline
- `build.sh`: Production build script
- `.gitignore`: Git ignore patterns

## Environment Variables
See `.env` or Replit secrets for:
- SECRET_KEY
- GEMINI_API_KEY
- YOUTUBE_API_KEY
- BREVO_API_KEY
- RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
- GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET
- CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
- DATABASE_URL (auto-provided by Replit)
