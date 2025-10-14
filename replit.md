# Kiri.ng - Nigerian Artisan Marketplace & Learning Platform

## Overview

Kiri.ng is a comprehensive Django-based Progressive Web Application (PWA) that serves as a marketplace connecting Nigerian artisans with customers while providing AI-powered educational pathways for skill development. The platform combines e-commerce functionality, social learning features, community blogging, and intelligent customer service to create an ecosystem for artisan business growth.

The application targets Nigerian artisans and customers, offering localized features including multi-language support (English, Hausa, Igbo, Yoruba), state-specific location services, and business resources tailored to the Nigerian market.

## Recent Changes (October 14, 2025)

### Bug Fixes & Improvements
1. **Referral System Overhaul**: Switched from UUID-based referral codes to username-based referrals
   - Referral URLs now use format: `https://kiri.ng/users/signup/?ref=USERNAME`
   - Backward compatible with legacy UUID referral codes
   - Removed referral input field from signup form (URL-based only)
   - Fixed referral count tracking - now properly increments when users sign up
   
2. **Academy Dark Mode Fixes**: Improved dark mode support in Academy module pages
   - Fixed AI question card background to properly adapt to dark mode
   - Added custom `ai-question-card` CSS class for better theme support
   
3. **Academy Validation Enhancement**: Implemented AI-powered answer validation
   - Users can no longer submit nonsense text to unlock modules
   - Gemini AI validates that answers demonstrate actual understanding
   - Gracefully fails open if AI service is unavailable
   - Provides specific feedback on why answers are rejected
   - Better user guidance with examples in the reflection prompt

### Previous Features (October 11, 2025)
1. **AI Customer Service System**: 24/7 Gemini-powered chatbot with quick help guides and admin controls
2. **Push Notifications**: Web Push API integration for real-time alerts (all platforms except iOS)
3. **PDF Certificate Generation**: WeasyPrint integration with proper error handling (verified working - 187KB PDFs)
4. **ML Service Recommendations**: Re-enabled TF-IDF vectorization with fallback to random recommendations
5. **Analytics & Monetization**: Google Analytics and Google AdSense integration

### Technical Improvements
- Installed system dependencies for WeasyPrint (pango, cairo, gdk-pixbuf, libffi)
- Added comprehensive error handling for PDF generation with logging
- Enhanced AI customer service with conversation history tracking
- Added floating AI support button for easy access
- Improved error handling across referral flows (regular signup, social login)

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework & Structure

**Django Monolith Architecture**: The application uses Django 5.0.6 as a monolithic framework with app-based modularization. Each major feature (marketplace, academy, blog, users, notifications) is isolated into Django apps with clear separation of concerns.

**Rationale**: Django's batteries-included approach provides authentication, ORM, admin interface, and templating out of the box, reducing development time for an MVP while maintaining scalability through app modularity.

### Application Modules

**Marketplace App**: Handles artisan service listings, bookings, and storefront functionality. Uses a category-based organization with support for multiple images per service. Implements ML-based service recommendations using scikit-learn's TF-IDF vectorization and cosine similarity for content-based filtering.

**Academy App**: AI-powered learning pathway system that generates personalized educational content. Integrates Google Gemini 2.5 Flash for pathway generation, module content creation, and Q&A tutoring. Supports video integration via YouTube API and generates downloadable PDF certificates using WeasyPrint.

**Blog App**: Community content platform with CKEditor 5 integration for rich text editing. Implements comment system and supports header images for posts.

**Users App**: Extended Django authentication with custom Profile model supporting OAuth via django-allauth (Google), referral system, location verification, and email verification workflows.

**Notifications App**: In-app notification system with real-time updates accessible via context processors.

**Core App**: Houses base templates, AI customer service chatbot (Gemini-powered), privacy/terms pages, and shared utilities.

### Authentication & Authorization

**Multi-Provider Authentication**: Supports traditional username/password signup with reCAPTCHA validation alongside Google OAuth via django-allauth. Custom adapters handle referral code capture during social login.

**Profile System**: One-to-one relationship with Django User model, storing artisan verification status, location data (verified via GPS), social media links, certificates, and referral tracking.

**Pros**: Flexible authentication reduces barriers to entry; social login improves conversion rates.
**Cons**: Multiple auth paths require careful session management and referral code handling.

### AI & Machine Learning Integration

**Google Gemini AI**: Primary AI service using gemini-2.0-flash-exp model for:
- Learning pathway outline generation based on user goals, skills, and location
- Module content generation with markdown formatting
- AI tutoring for module-specific questions
- Customer service chatbot with platform context awareness

**YouTube Integration**: Fetches relevant educational videos using YouTube Data API v3 with intelligent deduplication and relevance filtering.

**Service Recommendations**: Content-based filtering using TF-IDF and cosine similarity to suggest related services within categories.

**Rationale**: Gemini provides cost-effective, high-quality AI generation compared to alternatives like OpenAI. Content-based filtering offers accurate recommendations without requiring user interaction history.

### Data Storage & Media

**Database**: Default Django ORM with SQLite for development (production likely uses PostgreSQL based on typical Django deployments).

**File Storage**: Cloudinary for production media storage (profile pictures, service images, certificates, blog headers) with automatic optimization. Image validation enforces 2MB size limits.

**Static Files**: Managed via Django's collectstatic with separate static/ and staticfiles/ directories. Includes PWA manifest and service worker for offline functionality.

**PDF Generation**: WeasyPrint for certificate generation with system dependencies (pango, cairo, gdk-pixbuf, libffi) installed. Includes error handling with HTML fallback for reliability.

### Email & Notifications

**Brevo (Sendinblue) Integration**: Email delivery via django-anymail with Brevo backend for:
- Booking confirmations (artisan and customer notifications)
- Email verification links
- Referral notifications
- General system emails

**In-App Notifications**: Database-backed notification system with unread counts available globally via context processors. Auto-marks as read when notification page is viewed.

**Push Notifications**: Web Push API integration via service worker (works on all platforms except iOS). Includes subscription management and permission handling.

**AI Customer Service**: 24/7 intelligent chatbot powered by Google Gemini AI with:
- Conversational support with context awareness
- Quick help guides for common tasks (find service, create pathway, list service, refer friends, edit profile)
- Platform statistics integration for informed responses
- Admin control capabilities for elevated queries
- Accessible via floating action button and user menu

### Progressive Web App (PWA)

**Offline Capability**: Service worker implements cache-first strategy for static assets with network fallback. Caches key CSS, JS, and image assets.

**Installability**: manifest.json defines app metadata, icons, and shortcuts for "Add to Home Screen" functionality.

**Theme Support**: JavaScript-based dark/light mode toggle with localStorage persistence.

**Rationale**: PWA approach provides native-like experience without app store deployment, critical for Nigerian users with varying device capabilities.

### Frontend Architecture

**Template System**: Django templates with Bootstrap 5.3.3 for responsive UI. Custom CSS for theming with CSS variables for color schemes.

**Rich Text Editing**: CKEditor 5 for blog posts and academy content with custom configuration.

**Internationalization**: Django's i18n framework with gettext for multi-language support.

**Analytics & Monetization**: Google Analytics and AdSense integration via environment variables with conditional loading.

### Security & Validation

**reCAPTCHA v2**: Protects signup and login forms against bot abuse using django-recaptcha.

**CSRF Protection**: Django's built-in CSRF middleware with trusted origins configured for production domains and Replit environment.

**File Validation**: Custom validators ensure image uploads don't exceed 2MB, preventing storage abuse.

**Email Verification**: UUID-based token system for email confirmation before full account activation.

**Location Verification**: GPS-based verification for artisan storefronts to ensure accurate location data.

## External Dependencies

### Third-Party APIs

**Google Gemini AI** (google-generativeai): Core AI functionality for content generation, tutoring, and customer service. Requires GEMINI_API_KEY environment variable.

**YouTube Data API v3** (google-api-python-client): Video content discovery for learning modules. Requires YOUTUBE_API_KEY environment variable.

**Brevo (Sendinblue)** (django-anymail): Transactional email delivery. Requires BREVO_API_KEY environment variable.

**Google OAuth** (django-allauth): Social authentication provider.

**Google Analytics & AdSense**: Analytics tracking and monetization (optional, configured via environment variables).

### Python Libraries

**Core Framework**:
- Django 5.0.6: Web framework
- djangorestframework 3.16.1: API capabilities (potential future use)

**AI & ML**:
- google-generativeai 0.8.5: Gemini AI SDK
- scikit-learn (implied by imports): ML-based recommendations
- numpy 2.3.3: Numerical operations

**Content & Media**:
- django-ckeditor-5 0.2.18: Rich text editor
- WeasyPrint (via dependencies): PDF generation for certificates
- Pillow 11.3.0: Image processing

**Authentication & Security**:
- django-allauth (implied): Social authentication
- django-recaptcha: Bot protection

**Email**:
- django-anymail 13.1: Email backend abstraction

### Infrastructure Requirements

**Environment Variables**: The application requires numerous API keys and configuration values managed via python-decouple for secure .env loading.

**Static File Serving**: Requires collectstatic execution for production deployments.

**Database**: Currently SQLite (development), designed for PostgreSQL migration (production).

**Media Storage**: Local filesystem storage (may require cloud storage like AWS S3 for production scaling).

### Design Decisions

**Why Gemini over OpenAI**: Cost-effectiveness for startup MVP, competitive quality for educational content generation, and generous free tier for development.

**Why Django over FastAPI/Flask**: Rapid development with built-in admin, ORM, and authentication; mature ecosystem for full-stack applications; better suited for server-rendered pages with SEO requirements.

**Why Monolith over Microservices**: Simpler deployment and maintenance for MVP stage; easier debugging and development; sufficient for current scale with clear app boundaries enabling future service extraction if needed.

**Why PWA over Native Apps**: Single codebase for all platforms; no app store approval delays; easier updates; lower development cost; works well for Nigerian market with varied devices.