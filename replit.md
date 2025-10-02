# Kiri.ng - Nigerian Artisan Marketplace

## Overview
Kiri.ng is a comprehensive Django-based platform designed to empower Nigerian artisans by connecting them with customers, providing educational resources through the Academy, and fostering community engagement through blogging.

## Project Structure

### Apps
- **core**: Main application handling home pages and core functionality
- **users**: User authentication, profiles, and artisan storefronts
- **marketplace**: Service listings, bookings, and artisan dashboards  
- **academy**: Learning pathways and educational modules
- **blog**: Community blogging platform
- **notifications**: Real-time notification system

### Key Features
✅ User authentication with email verification
✅ Artisan verification system with location-based verification
✅ Service marketplace with category filtering
✅ Booking system with email notifications
✅ Educational academy with learning pathways
✅ Community blog with commenting
✅ Multi-language support (English, Hausa, Igbo, Yoruba)
✅ Dark/Light mode theming
✅ Social media integration for artisans
✅ Certificate display for verified artisans
✅ Multiple image upload for services
✅ Google reCAPTCHA for signup/login security
✅ Terms of Service acceptance requirement
✅ Referral system

## Recent Changes (October 2025)

### Environment Setup
- Upgraded to Python 3.12
- Installed all dependencies including django-recaptcha
- Environment variables configured via .env file
- Database migrations completed

### Latest UI/UX Improvements (Oct 2, 2025)
- ✅ **Dark Mode Overhaul**: Comprehensive dark mode text visibility fixes
  - Form labels, placeholders, and text inputs fully visible
  - List groups, pagination, tables, and modals styled correctly
  - Headings, paragraphs, and hr elements properly themed
  - Button close icons inverted for visibility
- ✅ **Header Redesign**: 
  - Logo increased from 70px to 85px for better visibility
  - Language selector moved directly under logo
  - Compact, flatter language selector design
  - Better space utilization on small screens
- ✅ **Artisan Storefront Beautification**:
  - Beautiful certificate sections with professional styling
  - Academy certificates with download buttons for completed pathways
  - Icons, badges, and improved card layouts
  - Efficient database queries (no N+1 issues)
  - Separate sections for professional and Academy certifications

### Previous UI/UX Improvements
- ✅ Replaced text logo with actual logo images (logo-dark.png, logo-light.png)
- ✅ Enhanced dark mode support across all pages
- ✅ Logo switches automatically based on theme
- ✅ Improved dark mode styling for headers, footers, and cards

### API & Backend Updates (Oct 2, 2025)
- ✅ **Google Gemini API**: Updated to gemini-2.5-flash model
  - Previous model (gemini-2.0-flash-exp) discontinued
  - Updated in both generate_module_content and generate_pathway_outline
- ✅ **Multiple Social Links**: Fixed CRUD functionality in profile editing
  - Create, update, and delete multiple social media links
  - Proper handling of removed links

### Security Enhancements
- ✅ Added Google reCAPTCHA to signup and login forms
- ✅ Made Terms & Conditions acceptance mandatory during signup
- ✅ Environment variables properly secured in .env file

### Feature Additions
- ✅ Added "Post New Service" to profile dropdown menu
- ✅ Booking counts now only visible to service owners (not public)
- ✅ Multiple image upload support for service creation
- ✅ Social media link management with inline formsets
- ✅ Professional certificate display on artisan storefronts
- ✅ Academy certificate display with download buttons

### Deployment Readiness (Oct 2, 2025)
- ✅ **Render Configuration**: render.yaml updated to Python 3.12.0
- ✅ **Professional README**: Comprehensive documentation created
  - Installation instructions
  - Deployment guide for Render
  - Feature documentation
  - Technology stack details
  - Project structure overview
- ✅ All deployment files verified (build.sh, gunicorn, psycopg2, whitenoise)

### Footer Enhancement
- ✅ Added developer credit with GitHub link to Nwokike

### Code Organization
- CSS properly organized in static/css/custom.css with comprehensive dark mode rules
- JavaScript organized in static/js/custom.js
- Separate auth_forms.py for authentication forms
- All features enabled (CKEditor, WeasyPrint, Scikit-learn)
- Efficient database queries with Django annotations

## Technology Stack
- **Backend**: Django 5.0.6
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Bootstrap 5.3.3, Vanilla JavaScript
- **Email**: Brevo (Anymail integration)
- **AI/ML**: Google Gemini API, YouTube API, Scikit-learn
- **Rich Text**: CKEditor 5
- **PDF Generation**: WeasyPrint
- **Captcha**: django-recaptcha

## Environment Variables
```
SECRET_KEY=<django-secret-key>
GEMINI_API_KEY=<google-gemini-api-key>
YOUTUBE_API_KEY=<youtube-api-key>
BREVO_API_KEY=<brevo-email-api-key>
DEFAULT_FROM_EMAIL=<sender-email>
RECAPTCHA_PUBLIC_KEY=<recaptcha-site-key>
RECAPTCHA_PRIVATE_KEY=<recaptcha-secret-key>
DEBUG=True
```

## Database Configuration
- Development: SQLite (db.sqlite3)
- Production: PostgreSQL (via DATABASE_URL environment variable)
- Automatic fallback to SQLite if PostgreSQL unavailable

## Running the Application
```bash
python manage.py runserver 0.0.0.0:5000
```

## Static Files
```bash
python manage.py collectstatic --noinput
```

## Deployment
- Configured for Render/Railway deployment
- Gunicorn for production WSGI server
- WhiteNoise for static file serving
- Build script available in build.sh

## User Preferences
- Python version: 3.12
- Database: SQLite for development, PostgreSQL for production
- Logo files: static/logo-light.png and static/logo-dark.png
- Developer: Nwokike (https://github.com/nwokike)

## Notes
- Service worker configured for PWA functionality
- Google Translate widget integrated for multi-language support
- Responsive design with mobile-first approach
- Bottom navigation for key sections (Services, Academy, Blog)
