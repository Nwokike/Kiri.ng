# Kiri.ng - Nigerian Artisan Marketplace

## Overview

Kiri.ng is a comprehensive Django-based Progressive Web App designed to empower Nigerian artisans by connecting them with customers, providing AI-powered educational resources, and fostering community engagement. The platform consists of three main modules:

1. **Marketplace** - A service listing and booking platform where artisans can showcase their skills and customers can find and book services
2. **Academy** - An AI-powered learning platform that generates personalized learning pathways using Google Gemini AI, helping artisans master new skills and grow their businesses
3. **Blog** - A community blogging platform where verified artisans can share knowledge, tutorials, and stories

The application is built with mobile-first design principles, supports Progressive Web App installation, includes dark/light theme switching, and offers multi-language support (English, Hausa, Igbo, Yoruba).

## Recent Changes (October 2025)

### Latest Update (October 11, 2025)
- **Comprehensive Dark Mode Audit**: Fixed all dark mode responsiveness issues across the entire application
  - AI-generated Academy content now properly displays in dark mode
  - Fixed hardcoded `bg-white`, `bg-light`, and `text-dark` classes throughout templates
  - Marketplace service cards, profile edit sections, and navigation now fully responsive
  - All CSS now uses CSS custom properties (--light-bg, --light-card, --light-text) for proper theming
- **Referral System Overhaul**: Implemented URL-based referral system working for ALL signup methods
  - Added unique `referral_code` field to Profile model (UUID-based, auto-generated)
  - Referral links format: `https://kiri.ng/users/signup/?ref=CODE`
  - Works for both form signup AND Google OAuth signup via custom adapters
  - Backward compatible with username-based referrals
  - Created database migration for existing users
- **Account Linking**: Google OAuth users and form users can now link accounts using the same email
- **Ask AI Enhancement**: Added JavaScript loading indicator showing "20 seconds" for AI question submissions
- **PWA Theme**: Changed manifest theme color from blue to green (#2c5530)
- **Authentication Improvements**: Custom Django Allauth adapters for OAuth and account management

### Previous Updates

#### UI/UX Improvements  
- **Dark Mode Enhancement**: Updated dark mode color scheme from pure black (#121212) to a softer dark blue-gray (#1a1a2e) for better eye comfort and integration with Google Translate widget
- **Academy Video Layout**: Reorganized YouTube video placement in learning pathways - all videos now appear at the top in a clean grid layout before written content, instead of being scattered throughout
- **Logo Update**: Replaced light mode logo and regenerated all favicons (16x16, 32x32, 48x48) and PWA icons

#### Authentication & Security
- **Password Reset**: Redesigned password reset email template to match the professional branded style of other transactional emails
- **Profile Security Settings**: Added dedicated "Security Settings" section in profile edit page with password reset option for easier access
- **Django Allauth Update**: Fixed deprecation warning by updating from ACCOUNT_AUTHENTICATION_METHOD to ACCOUNT_LOGIN_METHODS

#### Technical Updates
- **Python 3.12.11**: Confirmed running on Python 3.12+ as required
- **Favicon Generation**: Automated favicon creation using Pillow library for consistent branding across all platforms
- **Code Quality**: Fixed Django Allauth configuration deprecation warning for future compatibility

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture

**Framework**: Django 5.0.6 with Python
- **Monolithic Architecture**: Single Django project with modular app structure
- **Apps**: `core`, `users`, `marketplace`, `academy`, `blog`, `notifications`
- **Authentication**: Hybrid approach using both Django's built-in auth and Django Allauth for OAuth
  - Traditional email/password signup with email verification
  - Google OAuth integration for passwordless login
  - Password reset flow with branded email templates
- **Data Models**: Relational database design using Django ORM
  - User profiles with location verification
  - Service listings with multiple images
  - AI-generated learning pathways with modular content
  - Blog posts with rich text editing
  - Notification system for user engagement

### Frontend Architecture

**Template Engine**: Django Templates with Bootstrap 5.3.3
- **Progressive Web App**: Includes manifest.json and service worker for offline capabilities
- **Responsive Design**: Mobile-first approach with bottom navigation bar
- **Theme System**: CSS custom properties for light/dark mode switching with localStorage persistence
- **Rich Text Editing**: CKEditor 5 integration for blog posts and content creation
- **Translation**: Google Translate integration for multi-language support

### AI Integration

**Google Gemini 2.5 Flash**: Powers the Academy learning pathways
- **Pathway Generation**: Creates structured learning modules based on user goals, trade category, and location
- **Content Generation**: Generates written educational content for each module
- **AI Tutor**: Answers user questions about specific modules
- **YouTube Integration**: Uses YouTube Data API v3 to fetch relevant educational videos (2 per module)
- **Personalization**: Considers user's state/location for localized business advice

### Data Storage

**Database**: Not explicitly configured in settings (likely SQLite for development, PostgreSQL recommended for production)
- User profiles and authentication
- Service listings with images
- Learning pathways and module content
- Blog posts and comments
- Notifications and user activity

**File Storage**: Django's default file storage system
- Profile pictures (max 2MB)
- Service images (primary + additional images)
- Blog header images
- Certificate uploads

### Email System

**Django Anymail with Brevo (formerly Sendinblue)**
- Transactional emails for user verification
- Password reset emails
- Booking notifications to artisans
- Branded HTML email templates
- Support contact form submissions

### External Services & APIs

**Google Services**:
- Google Gemini AI (2.5 Flash) - Learning pathway and content generation
- YouTube Data API v3 - Educational video discovery
- Google OAuth - User authentication
- Google Analytics - Usage tracking (ID configured but implementation in templates)

**Security**:
- reCAPTCHA v2 - Bot protection on signup and login forms
- CSRF protection with trusted origins for Replit deployment

### Authentication & Authorization

**User Verification System**:
- Email verification tokens (UUID-based)
- Location-based artisan verification using GPS coordinates and reverse geocoding
- Artisan status verification for platform features (blogging, academy access)

**Social Authentication**:
- Django Allauth for Google OAuth
- No email verification required for OAuth signups
- Automatic profile creation on signup

### Notification System

**In-App Notifications**:
- Database-backed notification model
- Real-time unread count in navigation
- Notifications for bookings, referrals, and community activity
- Mark-as-read functionality

### Progressive Web App Features

**PWA Implementation**:
- Service worker for offline caching
- Web app manifest with icons and shortcuts
- Install prompt with custom UI
- Theme color integration with app branding

### Referral System

**Built-in Referral Tracking**:
- Username-based referral codes
- Referral relationship stored in user profiles
- Notification to referrer on successful signup
- Referral count displayed in user dashboard

### Form Validation & Security

**File Upload Validation**:
- Consistent 2MB file size limit across all image uploads
- Custom validators for profile pictures, service images, and blog headers
- reCAPTCHA integration on authentication forms

### Content Management

**Blog System**:
- CKEditor 5 for WYSIWYG editing
- Draft/Published workflow
- Header image support
- Comment system with moderation
- Category-based organization
- Slug-based URLs with date hierarchy

**Academy Content**:
- Markdown support for written content
- YouTube video embedding (2 videos per module interspersed with text)
- Progress tracking with module completion
- PDF certificate generation (WeasyPrint - currently disabled due to dependency issues)
- Community pathway sharing

### Design Patterns

**Key Architectural Decisions**:

1. **AI-First Learning**: Uses Google Gemini to generate personalized pathways instead of pre-built courses, allowing infinite scalability and customization

2. **Location-Aware Platform**: GPS-based verification helps build trust and enables location-specific business advice

3. **Multi-Image Service Listings**: Artisans can upload multiple images to better showcase their work, improving conversion rates

4. **Hybrid Authentication**: Supports both traditional signup and OAuth to maximize accessibility

5. **Notification-Driven Engagement**: In-app notifications keep users engaged with bookings, comments, and referral activity

6. **Mobile-First PWA**: Bottom navigation and install prompt optimize for mobile artisans who primarily use smartphones

7. **Theme Customization**: CSS custom properties enable consistent theming across light/dark modes

8. **Modular Django Apps**: Each feature area is isolated for maintainability and potential microservices migration

## External Dependencies

### Core Dependencies
- **Django 5.0.6** - Web framework
- **djangorestframework 3.16.1** - API support
- **django-allauth** - OAuth authentication
- **django-anymail 13.1** - Email backend (Brevo/Sendinblue)
- **django-ckeditor-5 0.2.18** - Rich text editor
- **django-recaptcha** - Bot protection
- **python-decouple** - Environment variable management

### AI & Machine Learning
- **google-generativeai 0.8.5** - Gemini AI integration
- **google-api-python-client 2.182.0** - YouTube API
- **scikit-learn** (sklearn) - Service recommendation engine (currently disabled due to version mismatch)

### File Processing
- **Pillow 11.3.0** - Image processing
- **WeasyPrint** (currently disabled) - PDF certificate generation
- **reportlab** - Alternative PDF generation

### Utilities
- **requests** - HTTP library for API calls
- **markdown 3.9** - Markdown parsing for academy content
- **python-dotenv** - Environment configuration

### Third-Party Services (API Keys Required)
- **Google Gemini API** - AI content generation
- **YouTube Data API v3** - Video search and embedding
- **Brevo (Sendinblue)** - Transactional email delivery
- **Google OAuth** - Social authentication
- **Google reCAPTCHA** - Form protection
- **Google Analytics** - Usage analytics (optional)

### Deployment Configuration
- **CSRF_TRUSTED_ORIGINS** - Configured for Replit deployment
- **ALLOWED_HOSTS** - Accepts all hosts (should be restricted in production)
- **Static Files** - Collected to `staticfiles/` directory
- **Media Files** - User uploads stored in `media/` directory

### Database Considerations
The application uses Django's default database settings (SQLite for development). For production deployment, PostgreSQL is recommended with proper database configuration in settings.py.