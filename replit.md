# Kiri.ng - Nigerian Artisan Marketplace & Learning Platform

## Overview

Kiri.ng is a Django-based Progressive Web Application (PWA) that connects Nigerian artisans with customers while providing AI-powered learning pathways for skill development. The platform serves two primary user types: artisans offering services and customers seeking services or learning new trades.

The application combines a service marketplace, AI-powered educational academy, community blog, and comprehensive user management into a single cohesive platform optimized for the Nigerian market.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Monolithic Django Architecture

The application follows a **modular monolithic architecture** where major features are isolated into separate Django apps:

- **academy** - AI-powered learning pathways with personalized module generation, progress tracking, and certificate generation
- **marketplace** - Service listings, booking system, and ML-based recommendations
- **blog** - Community content platform with rich text editing via CKEditor 5
- **users** - Authentication (email/password and Google OAuth), profile management, referral system, and location verification
- **notifications** - In-app notification system for user engagement
- **core** - Shared utilities, AI customer service chatbot, and SEO tools (sitemaps, IndexNow)

**Design Rationale**: Monolithic architecture was chosen for faster development, easier deployment, and reduced operational complexity in the Nigerian market. The PWA approach eliminates app store approval delays and provides cross-platform compatibility from a single codebase.

### AI Integration Architecture

**Google Gemini AI** (gemini-2.0-flash-exp model) powers multiple features:

- **Learning Pathway Generation**: Creates personalized module outlines based on user goals, location, and skill category
- **Dynamic Content Generation**: Produces detailed written educational content for each learning module on-demand
- **AI Tutoring**: Answers student questions within specific modules with context awareness
- **Quiz Generation**: Creates assessment questions for module validation
- **Customer Service Chatbot**: Provides 24/7 support with platform knowledge and ticket creation capability

**Machine Learning for Recommendations**:
- TF-IDF (Term Frequency-Inverse Document Frequency) vectorization analyzes service descriptions
- Cosine similarity calculations recommend related services
- Category-based filtering prioritizes same-category recommendations
- Implemented using scikit-learn for lightweight, effective recommendations without complex ML infrastructure

**Rationale**: Gemini was chosen for cost-effectiveness and quality compared to alternatives. On-demand content generation reduces storage requirements while maintaining flexibility. TF-IDF provides effective recommendations without requiring extensive training data or infrastructure.

### Authentication & User Management

**Multi-method Authentication**:
- Email/password with reCAPTCHA protection
- Google OAuth integration via django-allauth
- Session-based referral code tracking (supports both username and legacy code formats)

**Verification System**:
- Email verification with UUID tokens
- Location verification for artisan status (automatic based on street address and city)
- Verified artisans can list services and write blog posts

**Rationale**: Multiple authentication methods reduce signup friction. Location verification ensures service quality without manual admin approval overhead.

### Data Architecture

**Database**: PostgreSQL in production (Django ORM with standard relational schema)

**Key Models**:
- Users extended with Profile model (one-to-one relationship)
- Learning pathways with nested modules, videos, questions, and quizzes
- Services with category relationships and multiple images
- Bookings, blog posts with comments, notifications

**Media Storage**: Cloudinary integration for optimized image storage and delivery, reducing server storage requirements and improving performance across Nigeria's varying network conditions.

### Email & Communication

**Transactional Emails**: Brevo (Sendinblue) via django-anymail handles:
- Account verification emails
- Booking confirmations
- Password resets
- Referral notifications

**Push Notifications**: Web Push API for real-time alerts (excluding iOS due to platform limitations)

**Rationale**: Brevo provides reliable email delivery with good deliverability rates in Nigeria. Web Push API enables engagement without requiring native app infrastructure.

### PDF Generation

**WeasyPrint** generates downloadable certificates for completed learning pathways, converting HTML templates to PDF with custom styling and user information.

### SEO Architecture

**Sitemap System**: Dynamic XML sitemaps for static pages, blog posts, services, artisan profiles, and learning pathways

**IndexNow Integration**: Automatic submission of new/updated content to search engines (Bing, Yandex, Naver) for faster indexing

**Rationale**: Proactive SEO tools improve discoverability without manual intervention, critical for organic growth in the Nigerian market.

### Progressive Web App (PWA)

**Service Worker**: Caches critical assets for offline functionality and improved load times

**Manifest**: Defines installable app experience with shortcuts to key features (Services, Academy, Blog)

**Rationale**: PWA provides native-like experience without app store barriers, crucial for reaching users across diverse device capabilities in Nigeria.

## External Dependencies

### AI & APIs
- **Google Gemini API** (gemini-2.0-flash-exp) - AI content generation, tutoring, and chatbot
- **YouTube Data API v3** - Fetches educational videos for learning modules

### Authentication & Security
- **Google OAuth 2.0** - Social login via django-allauth
- **reCAPTCHA v2** - Spam protection for signup and login

### Email & Communication
- **Brevo (Sendinblue) API** - Transactional email delivery via django-anymail

### Media & Storage
- **Cloudinary** - Cloud-based media storage and optimization

### Analytics & Monetization
- **Google Analytics** - User behavior tracking
- **Google AdSense** - Ad monetization

### Python Libraries
- **Django 5.0.6** - Web framework
- **djangorestframework** - API endpoints
- **django-ckeditor-5** - Rich text editor for blog posts
- **django-allauth** - Social authentication
- **scikit-learn** - ML-based service recommendations
- **WeasyPrint** - PDF certificate generation
- **Pillow** - Image processing
- **python-decouple** - Environment variable management

### Frontend
- **Bootstrap 5.3.3** - Responsive UI framework
- **Bootstrap Icons** - Icon library
- **Vanilla JavaScript** - Client-side interactivity
- **CKEditor 5** - Rich text editing