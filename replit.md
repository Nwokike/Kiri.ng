# Kiri.ng - Nigerian Artisan Marketplace

## Overview

Kiri.ng is a comprehensive Django-based platform that empowers Nigerian artisans by connecting them with customers through a marketplace, providing AI-powered educational resources through an Academy, and fostering community engagement through blogging. The platform features location-based artisan verification, real-time notifications, booking systems, and progressive web app (PWA) capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Framework & Core Technologies

**Django 5.0.6** serves as the backend framework with a traditional monolithic architecture. The application uses Django's built-in ORM for database operations (designed to work with any database backend, though PostgreSQL is recommended for production). Static files are managed through WhiteNoise middleware for efficient serving.

**Why Django**: Chosen for its batteries-included philosophy, robust ORM, built-in admin interface, and strong security features. The monolithic approach simplifies deployment and maintenance for this stage of the project.

### Application Structure

The codebase follows Django's app-based architecture with clear separation of concerns:

- **Core**: Base templates, static assets, and shared utilities
- **Users**: Authentication, profiles, verification, and social media links
- **Marketplace**: Service listings, bookings, categories, and artisan storefronts
- **Academy**: AI-powered learning pathways with video integration
- **Blog**: Community content creation with rich text editing
- **Notifications**: Real-time user notifications system

**Design Pattern**: Each app is self-contained with its own models, views, forms, and templates. This modular approach allows for independent scaling and maintenance of features.

### Authentication & Authorization

Django's built-in authentication system is extended with:
- Custom user creation forms with reCAPTCHA protection
- Email verification using UUID tokens
- Location-based artisan verification through GPS coordinates
- Profile model linked one-to-one with User model

**Why This Approach**: Leverages Django's battle-tested auth system while adding domain-specific verification layers. The one-to-one profile pattern allows extending user data without modifying the core User model.

### AI Integration

**Google Gemini 2.5 Flash API** powers the Academy's personalized learning pathways:
- Generates structured learning modules based on user goals
- Creates custom content for each module
- Answers student questions contextually
- Adapts content based on Nigerian context and user location

**Implementation**: AI services are abstracted in `academy/ai_services.py` to allow easy provider switching. The system uses streaming responses for better user experience and implements error handling for API failures.

### Third-Party Content Integration

**YouTube Data API v3** provides educational video content:
- Searches for relevant videos per learning module
- Filters by quality and relevance
- Tracks used video IDs to avoid duplicates
- Falls back gracefully if API quota is exceeded

**Trade-off**: Relies on external API availability but provides rich multimedia content without hosting costs.

### Email System

**Brevo (formerly Sendinblue)** handles transactional emails via Django Anymail:
- Email verification on signup
- Booking confirmations to artisans
- Location verification notifications
- Blog comment notifications

**Why Brevo**: Offers reliable delivery, good free tier, and simple Django integration through Anymail abstraction layer.

### Rich Text Editing

**CKEditor 5** integration via `django-ckeditor-5` provides WYSIWYG editing for blog posts with:
- Image uploads
- Text formatting
- Table support
- Custom styling options

### Progressive Web App (PWA)

PWA implementation includes:
- Service worker for offline caching (`static/service-worker.js`)
- Web app manifest (`static/manifest.json`)
- Installable on mobile devices
- Offline fallback for core pages

**Benefits**: Native app-like experience without app store distribution, improved performance through caching, works on any device.

### Frontend Architecture

**Bootstrap 5** provides the UI framework with:
- Custom CSS variables for theme switching (`static/css/custom.css`)
- Dark/light mode with localStorage persistence
- Mobile-first responsive design
- Bottom navigation pattern for mobile UX

**JavaScript Organization**: Vanilla JavaScript for core functionality (no heavy frameworks), Google Translate integration for multi-language support (English, Hausa, Igbo, Yoruba).

### Data Models

**Key Relationships**:
- User → Profile (One-to-One): Extended user information
- User → Services (One-to-Many): Artisans create multiple services
- Service → Bookings (One-to-Many): Services receive multiple bookings
- User → LearningPathways (One-to-Many): Users create learning journeys
- LearningPathway → PathwayModules (One-to-Many): Structured learning content

**Media Handling**: Supports multiple images per service through `ServiceImage` model, profile pictures, certificates, and blog post headers with 2MB size validation.

### Security Measures

- Google reCAPTCHA v2 on signup/login
- CSRF protection on all forms
- Email verification required for activation
- UUID-based verification tokens
- WhiteNoise for secure static file serving
- Mandatory Terms of Service acceptance

## External Dependencies

### APIs & Services

1. **Google Gemini AI API** (`GEMINI_API_KEY`)
   - Purpose: Generate personalized learning content
   - Fallback: Graceful error messages if unavailable

2. **YouTube Data API v3** (`YOUTUBE_API_KEY`)
   - Purpose: Fetch educational videos for modules
   - Fallback: Modules work without videos, manual links possible

3. **Brevo Email API** (`BREVO_API_KEY`)
   - Purpose: Transactional email delivery
   - Integration: Django Anymail for abstraction

4. **Google reCAPTCHA** (`RECAPTCHA_PUBLIC_KEY`, `RECAPTCHA_PRIVATE_KEY`)
   - Purpose: Bot protection on authentication
   - Version: v2 Checkbox

5. **Google Translate Widget**
   - Purpose: Multi-language support
   - Integration: Client-side widget

6. **Google Analytics** (`GOOGLE_ANALYTICS_ID`)
   - Purpose: User behavior tracking

7. **Google AdSense** (`GOOGLE_ADSENSE_ID`)
   - Purpose: Monetization

### Python Libraries

**Core Framework**:
- Django 5.0.6: Web framework
- djangorestframework 3.16.1: API capabilities (future use)

**AI & ML**:
- google-generativeai 0.8.5: Gemini AI integration
- google-api-python-client 2.182.0: YouTube API

**Content & Media**:
- django-ckeditor-5 0.2.18: Rich text editing
- Pillow 11.3.0: Image processing
- Markdown 3.9: Markdown rendering

**Email**:
- django-anymail 13.1: Email service abstraction

**Security**:
- django-recaptcha: Form protection
- cryptography 46.0.1: Encryption utilities

**Frontend Assets**:
- Bootstrap 5 (via CDN)
- Font Awesome icons (via CDN)

### Database

The application uses Django ORM without database-specific dependencies, allowing flexibility in database choice. Recommended setup:
- **Development**: SQLite (Django default)
- **Production**: PostgreSQL (for better performance and features)

No Drizzle or explicit database drivers in requirements suggest using Django's built-in database abstraction.

### File Storage

- **Development**: Local filesystem (`MEDIA_ROOT`)
- **Production Ready**: Can integrate with cloud storage (S3, Cloudinary) through Django storage backends

### Deployment Considerations

- WhiteNoise configured for static files
- Environment variables via python-dotenv
- DEBUG mode controlled by environment
- ALLOWED_HOSTS set to accept all (should be restricted in production)
- No specific WSGI server in requirements (gunicorn/uwsgi should be added for production)