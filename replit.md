# Kiri.ng - Nigerian Artisan Marketplace & Learning Platform

## Overview

Kiri.ng is a Django-based Progressive Web Application (PWA) that connects Nigerian artisans with customers while providing AI-powered learning pathways for skill development. The platform combines a service marketplace, an educational academy powered by Google Gemini AI, a community blogging system, and real-time engagement features.

The application serves two primary user types:
- **Artisans**: Professionals offering services, managing bookings, and building their skills
- **Customers**: Users seeking artisan services and learning new trades

## Recent Changes

### October 15, 2025
- **Blog CKEditor Improvements**: Fixed image upload functionality with custom CSRF-exempt endpoint; added meta description and category fields to post creation form
- **Blog Category Navigation**: Implemented category filtering in blog views with navigation display
- **SEO Enhancements**: Fixed sitemap to only include published posts; integrated IndexNow for automatic search engine indexing
- **Marketplace UI Redesign**: Redesigned service browsing with compact cards, grid/list view toggle, and filtering by location and category
- **Academy Public Access**: Made learning pathway module content (videos, written content, steps) fully accessible to guest users to encourage sign-ups

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Monolithic Django Architecture

The application follows a **modular monolithic architecture** where each major feature is isolated into separate Django apps. This provides clear separation of concerns while maintaining the simplicity of a single deployable unit.

**Core Django Apps:**
- `academy` - AI-powered learning pathways and skill development
- `marketplace` - Service listings and booking system
- `blog` - Community content platform with CKEditor integration
- `users` - Authentication, profiles, and referral system
- `notifications` - In-app notification system
- `core` - Shared utilities, AI customer service, and SEO tools

**Design Rationale:**
- Monolithic architecture chosen for faster development and easier deployment in the Nigerian market
- PWA approach eliminates app store delays and provides cross-platform compatibility
- Single codebase reduces maintenance complexity

### AI & Machine Learning Integration

**Google Gemini AI** (gemini-2.0-flash-exp model) powers multiple features:
- **Learning Pathway Generation**: Creates personalized module outlines based on user goals, location, and skill category
- **Content Generation**: Produces detailed written content for each learning module
- **AI Tutoring**: Answers student questions within modules
- **Quiz Generation**: Creates assessment questions for module validation
- **Customer Service Chatbot**: Provides 24/7 support with context awareness

**Machine Learning for Recommendations:**
- TF-IDF (Term Frequency-Inverse Document Frequency) vectorization for service descriptions
- Cosine similarity calculations to recommend similar services
- Category-based filtering prioritizes same-category recommendations
- Implemented using scikit-learn

**Rationale:**
- Gemini chosen for cost-effectiveness and quality compared to alternatives
- TF-IDF provides effective recommendations without complex ML infrastructure
- On-demand content generation reduces storage requirements

### Authentication & User Management

**Multi-Provider Authentication:**
- Email/password registration with Django's built-in auth
- Google OAuth via django-allauth
- reCAPTCHA v2 protection on signup/login forms
- Email verification system using UUID tokens

**Referral System:**
- Username-based referral codes (replaces legacy UUID system)
- Session persistence for referral tracking across signup methods
- Automatic referrer notification on successful registration
- Backward compatibility with old referral codes

**Profile System:**
- GPS-based location verification (city/state)
- Artisan verification badges
- Social media links (Instagram, Facebook, WhatsApp Business)
- Multi-image portfolio for artisan services

**Design Decisions:**
- Username-based referrals are more user-friendly than UUIDs
- Email verification prevents spam accounts
- reCAPTCHA balances security with user experience
- Separate verified/unverified location fields allow manual overrides

### Database Architecture

**PostgreSQL Production Database:**
- Primary data store in production
- Relational model with foreign key constraints
- Indexed fields for performance (publish dates, created_at)

**Key Models & Relationships:**
- `User` (Django auth) → `Profile` (1:1)
- `User` → `Service` (1:Many) for artisan listings
- `User` → `LearningPathway` (1:Many) for personalized learning
- `LearningPathway` → `PathwayModule` (1:Many) → `ModuleVideo` (1:Many)
- `Service` → `Booking` (1:Many) for customer requests
- `Post` → `Comment` (1:Many) for blog interactions

**Data Generation Strategy:**
- AI-generated content stored as text fields rather than files
- YouTube video links stored as URLs (no local storage)
- Images handled via Cloudinary integration

### Content Management

**CKEditor 5 Integration:**
- Rich text editing for blog posts
- Custom image upload handler bypassing CSRF (required for CKEditor 5)
- Direct Cloudinary upload for embedded images
- 2MB file size limit enforced at application level

**File Validation:**
- Reusable `validate_image_size` function across forms
- Client-side and server-side validation
- Cloudinary handles optimization and CDN delivery

**SEO Optimization:**
- Auto-generated meta descriptions with 160-character limit
- URL slugs for posts, services, and learning pathways
- Django sitemaps for all major content types
- IndexNow API integration for instant search engine indexing

### Real-Time Features

**Notification System:**
- Database-backed notification model
- Context processor provides unread count globally
- Auto-mark as read when viewing notification list
- Triggered by: bookings, referrals, comments, module completions

**Push Notifications:**
- Web Push API integration (excludes iOS due to platform limitations)
- Service worker registration in base template
- PWA manifest for installability

**Design Trade-offs:**
- Database notifications chosen over WebSockets for simplicity
- iOS limitation acknowledged due to Web Push API restrictions
- Service worker provides offline capability

### Email System

**Brevo (Sendinblue) Integration:**
- Transactional emails via django-anymail
- Email verification links
- Booking confirmations to artisans and customers
- Referral success notifications
- Password reset flows

**Email Templates:**
- HTML templates with inline CSS for compatibility
- Responsive design using table-based layouts
- Branded header with logo
- Call-to-action buttons

**Rationale:**
- Brevo chosen for reliability and deliverability
- Transactional focus (no marketing automation needed)
- django-anymail provides abstraction layer

### PDF Generation

**WeasyPrint for Certificates:**
- Server-side PDF rendering from HTML templates
- Base64-encoded logo embedding for offline rendering
- Custom certificate template with user details
- Download triggered on pathway completion

**Design Considerations:**
- WeasyPrint chosen over alternatives for Django compatibility
- HTML/CSS approach allows easy template customization
- Base64 images eliminate external file dependencies

### Media Storage

**Cloudinary Integration:**
- Production media storage and CDN
- Automatic image optimization
- Profile pictures, service images, blog headers, certificates
- CKEditor embedded images

**Local Development:**
- Local file system for media during development
- Environment-based configuration switching

### Internationalization (i18n)

**Multi-Language Support:**
- English (default)
- Hausa
- Igbo  
- Yoruba

**Implementation:**
- Django's `gettext_lazy` for translatable strings
- Localized form labels and help text
- Context-aware translations

**Rationale:**
- Targets major Nigerian language groups
- Improves accessibility in rural areas
- Future expansion to French (for West African neighbors)

### Progressive Web App (PWA)

**Manifest Configuration:**
- Standalone display mode
- Custom icons for light/dark themes
- Shortcuts to Services and Academy
- Installable on all platforms

**Service Worker:**
- Cache-first strategy for static assets
- Network-first for dynamic content
- Offline fallback capability
- Cache versioning (CACHE_NAME)

**Design Philosophy:**
- Native-like experience without app stores
- Instant updates without approval delays
- Single codebase for all platforms

## External Dependencies

### AI & APIs

- **Google Gemini AI** (`google-generativeai==0.8.5`)
  - Purpose: Content generation, tutoring, chatbot
  - API Key: `GEMINI_API_KEY` environment variable
  
- **YouTube Data API v3** (`google-api-python-client==2.182.0`)
  - Purpose: Fetch relevant video tutorials for modules
  - API Key: `YOUTUBE_API_KEY` environment variable

### Email Service

- **Brevo/Sendinblue** (`django-anymail==13.1`)
  - Purpose: Transactional email delivery
  - API Key: `BREVO_API_KEY` environment variable
  - Backend: `anymail.backends.sendinblue.EmailBackend`

### Media & Storage

- **Cloudinary**
  - Purpose: Image hosting, optimization, CDN delivery
  - Configuration: Environment variables for cloud name, API key, secret
  - Note: Configuration details not visible in provided files

### Security & Authentication

- **Google OAuth** (`django-allauth`)
  - Purpose: Social authentication
  - Configuration: OAuth client credentials in environment

- **reCAPTCHA v2** (`django-recaptcha`)
  - Purpose: Bot prevention on forms
  - Keys: `RECAPTCHA_PUBLIC_KEY`, `RECAPTCHA_PRIVATE_KEY`

### Analytics & Monetization

- **Google Analytics**
  - Tracking ID: `GOOGLE_ANALYTICS_ID` environment variable
  
- **Google AdSense**
  - Client ID: `GOOGLE_ADSENSE_CLIENT_ID` environment variable

### SEO & Indexing

- **IndexNow Protocol**
  - Purpose: Instant search engine indexing
  - Supported: Bing, Yandex, Naver
  - Key: Auto-generated from Django secret key if not provided

### Machine Learning

- **Scikit-learn** (`scikit-learn` implied by usage)
  - TF-IDF vectorization
  - Cosine similarity calculations
  - Service recommendation engine

### Database

- **PostgreSQL** (production)
  - Configured via environment variables
  - Note: Application designed for Postgres but uses Django ORM (database-agnostic models)

### Content Editing

- **CKEditor 5** (`django-ckeditor-5==0.2.18`)
  - WYSIWYG editor for blog posts
  - Custom upload endpoint for image handling
  - Direct Cloudinary integration

### PDF Generation

- **WeasyPrint** (implied by usage in academy views)
  - HTML to PDF conversion
  - Certificate generation
  - Requires system dependencies (Cairo, Pango)

### Frontend Framework

- **Bootstrap 5.3.3** (CDN)
  - Responsive UI components
  - Mobile-first design
  - Dark/light theme toggle

### Environment Management

- **python-decouple** (`decouple`)
  - Secure environment variable handling
  - Configuration separation
  - Production/development switching