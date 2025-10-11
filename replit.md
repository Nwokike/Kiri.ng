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

## Recent Changes (Oct 11, 2025)
### ✅ Comprehensive Audit & Improvements Completed
All audit findings have been addressed and improvements implemented:

1. **Logging System Upgrade**
   - Replaced all debug print() statements with proper Django logging
   - Files updated: academy/ai_services.py, academy/views.py, marketplace/recommender.py, users/views.py
   - Using module-level loggers: `logger = logging.getLogger(__name__)`

2. **Modern JavaScript APIs**
   - Updated clipboard API from deprecated execCommand to modern Clipboard API
   - Feature detection with graceful fallback for older browsers
   - Mobile-friendly implementation in static/js/dashboard.js

3. **Code Cleanup**
   - Removed unused ModuleStep creation logic from academy/views.py
   - Cleaned up all duplicate *_old.html template files

4. **Model Improvements**
   - Added consistent Meta classes to Profile, Service, and Booking models
   - Better admin UX with verbose names and proper ordering

5. **Email System Overhaul** ⭐
   - Created responsive email_base.html template with inline CSS
   - Rebuilt all 4 email templates with professional design:
     * welcome_artisan_email.html
     * email_verification.html
     * password_reset_email.html
     * booking_notification_email.html
   - Email client compatible (Gmail, Outlook, mobile)
   - Branded headers with logo, mobile-responsive layout

6. **UI Enhancements**
   - Changed referral code to "Generate Referral Code" button (cleaner UX)
   - Button reveals code on click with modern copy functionality

### Previous Fixes
- Fixed critical datetime import bug in Certificate.is_expired property
- Removed duplicate Comment import in academy/forms.py
- Configured deployment for Gunicorn with autoscale

## Project Structure
See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed file tree.

```
kiriong/          # Main Django settings
├── academy/      # AI learning platform
├── blog/         # Community blogging
├── core/         # Home, support, base templates
├── marketplace/  # Services & bookings
├── notifications/# Real-time notifications
├── users/        # Profiles, auth, certificates
├── static/       # CSS, JS, images
└── templates/    # Global templates (incl. email_base.html)
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
- All logging uses Python's logging framework (no print statements)
- Email templates use responsive design with email client compatibility

## Documentation
- **AUDIT_FINDINGS.md**: Complete audit report with all improvements documented
- **PROJECT_STRUCTURE.md**: Detailed project tree and architecture
- **DEPLOYMENT_CHECKLIST.md**: Deployment guide and checklist

## Deployment
- **Target**: Autoscale deployment
- **Build**: `python manage.py collectstatic --noinput`
- **Run**: `gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=4 kiriong.wsgi:application`
- Production settings enforce HTTPS, secure cookies, HSTS
