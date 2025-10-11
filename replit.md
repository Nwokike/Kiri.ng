# Kiri.ng - Django PWA for Nigerian Artisans

## Project Overview
A comprehensive Progressive Web App empowering Nigerian artisans through:
- **Marketplace**: Service listings, bookings, artisan profiles
- **Academy**: AI-powered learning pathways with Gemini 2.5 Flash
- **Blog**: Community content sharing with CKEditor
- **Notifications**: Real-time updates for users
- **Authentication**: Google OAuth + traditional auth with email verification

## Tech Stack
- **Backend**: Django 5.0.6 + PostgreSQL
- **Frontend**: Bootstrap 5.3.3, Vanilla JS
- **AI**: Google Gemini 2.5 Flash, YouTube Data API v3
- **Email**: Brevo (django-anymail)
- **Storage**: Cloudinary
- **PWA**: Service workers, Web App Manifest
- **Auth**: Django Allauth, reCAPTCHA

## Recent Changes (Oct 2025)
- Fixed critical datetime import bug in Certificate.is_expired property
- Removed duplicate Comment import in academy/forms.py
- Configured deployment for Gunicorn with autoscale
- Comprehensive audit completed

## Project Structure
```
kiriong/          # Main Django settings
├── academy/      # AI learning platform
├── blog/         # Community blogging
├── core/         # Home, support, base templates
├── marketplace/  # Services & bookings
├── notifications/# Real-time notifications
├── users/        # Profiles, auth, certificates
├── static/       # CSS, JS, images
└── templates/    # Global templates
```

## Known Issues
1. **PDF Certificate Generation**: Disabled due to weasyprint/cffi compatibility issues
   - Currently returns HTML instead of PDF
   - TODO: Re-enable after fixing Python version compatibility
   
2. **Sklearn Recommendations**: Disabled due to import issues
   - Simple random recommendations implemented as fallback
   - TODO: Re-enable ML-based recommendations

## Database Models
- **Users**: Profile, SocialMediaLink, Certificate
- **Marketplace**: Category, Service, ServiceImage, Booking
- **Academy**: LearningPathway, PathwayModule, ModuleVideo, ModuleQuestion, Badge, UserBadge, Comment
- **Blog**: Post, Comment
- **Notifications**: Notification

## Environment Variables Required
- SECRET_KEY
- GEMINI_API_KEY
- YOUTUBE_API_KEY
- BREVO_API_KEY
- RECAPTCHA_PUBLIC_KEY / RECAPTCHA_PRIVATE_KEY
- GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET
- CLOUDINARY_CLOUD_NAME / CLOUDINARY_API_KEY / CLOUDINARY_API_SECRET
- DATABASE_URL (auto-provided by Replit)

## Development Notes
- Server runs on port 5000 (Django dev server)
- PostgreSQL database via Replit
- Static files served via WhiteNoise
- Dark/light mode with localStorage persistence
- Multi-language support (English, Hausa, Igbo, Yoruba)

## Deployment
- **Target**: Autoscale deployment
- **Build**: `python manage.py collectstatic --noinput`
- **Run**: `gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=4 kiriong.wsgi:application`
- Production settings enforce HTTPS, secure cookies, HSTS
