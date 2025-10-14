# Kiri.ng - Nigerian Artisan Marketplace & Learning Platform

![Kiri.ng Logo](static/logo-light.png)

## 🚀 [Live Site](https://kiri.ng/)

Kiri.ng is a comprehensive Django-based Progressive Web Application (PWA) connecting Nigerian artisans with customers. It features an innovative AI-powered learning academy, a community blog, and intelligent customer service to create a complete ecosystem for artisan growth.

-----

## ✨ Key Features

  * **🛒 Marketplace**: Service listings with a booking system, ML-based service recommendations, and artisan dashboards.
  * **🎓 AI Academy**: Personalized learning pathways powered by **Google Gemini**, progress tracking, AI tutoring, and downloadable PDF certificates.
  * **🤖 AI Customer Service**: A 24/7 Gemini-powered chatbot with quick help guides and conversation history.
  * **📝 Community Blog**: A rich content platform using CKEditor 5 for posts, complete with a commenting system.
  * **🔔 Real-Time Engagement**: In-app notifications and Web Push API for real-time alerts (excluding iOS).
  * **🎨 Modern User Experience**: A mobile-first, responsive PWA with a dark/light mode toggle and multi-language support (English, Hausa, Igbo, Yoruba).
  * **👤 Robust User System**: Secure sign-up with reCAPTCHA, Google OAuth, a username-based referral system, and detailed user profiles.

-----

## 🏗️ System Architecture

Kiri.ng is built using a **Django Monolithic Architecture**, where each major feature is isolated into a modular Django app for a clear separation of concerns. This approach streamlines development and deployment for the current scale.

### Core Components

  * **AI & Machine Learning**: We use **Google Gemini** for its cost-effectiveness and quality in generating learning pathways, module content, and powering our AI chatbot. Service recommendations are driven by a content-based filtering system using TF-IDF and cosine similarity.
  * **Data & Media**: The application is designed for a **PostgreSQL** production database and integrates with **Cloudinary** for optimized media storage. **WeasyPrint** is used for generating PDF certificates on the fly.
  * **Backend Services**: Transactional emails (confirmations, verification, etc.) are reliably handled by **Brevo (Sendinblue)** through `django-anymail`.
  * **Design Philosophy**: We chose a **PWA over a native app** to ensure a single codebase provides a native-like experience across all devices without app store delays, which is ideal for the Nigerian market.

-----

## 🛠 Tech Stack

  * **Backend**: Django 5.0.6, PostgreSQL, Gunicorn
  * **Frontend**: Bootstrap 5.3.3, Vanilla JS, CKEditor 5
  * **AI & APIs**: Google Gemini, YouTube Data API v3
  * **Services**: Brevo (email), Cloudinary (media), Google OAuth, reCAPTCHA
  * **ML**: Scikit-learn
  * **PDF Generation**: WeasyPrint

-----

## 🚀 Local Development Setup

### 1\. Clone & Install

```bash
git clone https://github.com/nwokike/kiri.ng.git
cd kiri.ng
pip install -r requirements.txt
```

### 2\. Configure Environment Variables

Create a `.env` file in the root directory and add the necessary keys.

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@host:port/database

# AI & APIs
GEMINI_API_KEY=your-gemini-api-key
YOUTUBE_API_KEY=your-youtube-api-key

# Email
BREVO_API_KEY=your-brevo-api-key
DEFAULT_FROM_EMAIL=noreply@kiri.ng

# Media Storage
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Google OAuth (optional)
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# reCAPTCHA (optional)
RECAPTCHA_PUBLIC_KEY=your-site-key
RECAPTCHA_PRIVATE_KEY=your-secret-key
```

### 3\. Setup Database & Static Files

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 4\. Run the Server

```bash
python manage.py runserver 0.0.0.0:5000
```

Visit **http://localhost:5000** in your browser.

-----

## 🗂️ Complete Project Structure

```
kiriong/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD pipeline for automated deployments
├── academy/                        # App: AI-powered learning platform
│   ├── migrations/                 # Database schema changes for the academy
│   ├── templates/
│   │   └── academy/                # Templates specific to the academy
│   │       ├── academy_home.html
│   │       ├── certificate.html
│   │       ├── create_pathway.html
│   │       ├── dashboard.html
│   │       ├── pathway_detail.html
│   │       ├── pathway_list.html
│   │       └── public_pathway_detail.html
│   ├── templatetags/               # Custom template filters and tags
│   ├── admin.py                    # Django admin configuration for academy models
│   ├── ai_services.py              # Handles all Google Gemini AI integrations
│   ├── apps.py                     # App-specific configuration
│   ├── forms.py                    # Forms for pathway creation, quizzes, etc.
│   ├── models.py                   # Data models (LearningPathway, Module, Badge)
│   ├── urls.py                     # URL routing for the academy
│   └── views.py                    # Logic for handling requests and rendering pages
├── blog/                           # App: Community blogging platform
│   ├── migrations/
│   ├── templates/
│   │   └── blog/
│   │       ├── post_detail.html
│   │       ├── post_form.html
│   │       └── post_list.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                    # Contains the CKEditor 5 form integration
│   ├── models.py                   # Data models (Post, Comment)
│   ├── urls.py
│   └── views.py
├── core/                           # App: Core functionality and shared components
│   ├── migrations/
│   ├── templates/
│   │   └── core/
│   │       ├── base.html           # The master base template for the entire site
│   │       ├── privacy.html
│   │       └── terms.html
│   ├── context_processors.py       # Provides global context (e.g., notification count)
│   ├── urls.py
│   └── views.py                    # Handles homepage, AI chatbot logic, etc.
├── kiriong/                        # Main Django project configuration
│   ├── asgi.py                     # ASGI entrypoint for async servers
│   ├── settings.py                 # Core project settings and configurations
│   ├── urls.py                     # Root URL configuration for the project
│   └── wsgi.py                     # WSGI entrypoint for traditional servers
├── marketplace/                    # App: Artisan services and bookings
│   ├── migrations/
│   ├── templates/
│   │   └── marketplace/
│   │       ├── artisan_dashboard.html
│   │       ├── booking_notification_email.html
│   │       ├── service_confirm_delete.html
│   │       ├── service_detail.html
│   │       ├── service_form.html
│   │       └── service_list.html
│   ├── templatetags/
│   ├── models.py                   # Data models (Category, Service, Booking)
│   ├── recommender.py              # ML logic for service recommendations
│   ├── urls.py
│   └── views.py
├── media/                          # User-uploaded files (development)
├── notifications/                  # App: In-app user notifications
│   ├── migrations/
│   ├── templates/
│   │   └── notifications/
│   │       └── notification_list.html
│   ├── models.py                   # Data model (Notification)
│   ├── urls.py
│   └── views.py
├── static/                         # Development static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   ├── icons/
│   │   ├── logo-dark.png
│   │   └── logo.png
│   ├── js/
│   │   ├── dashboard.js
│   │   └── theme-toggle.js
│   ├── manifest.json               # PWA manifest file
│   └── service-worker.js           # PWA service worker for offline capabilities
├── staticfiles/                    # Collected static files for production
├── templates/                      # Global templates (not tied to a specific app)
│   ├── account/                    # Templates for django-allauth
│   ├── registration/               # Templates for Django's built-in auth
│   └── email_base.html
├── users/                          # App: User management, profiles, and authentication
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   │       ├── certificates.html
│   │       ├── profile_detail.html
│   │       └── profile_edit.html
│   ├── models.py                   # Custom Profile model, Certificate, SocialMediaLink
│   ├── urls.py
│   └── views.py
├── .gitignore                      # Specifies files and folders for Git to ignore
├── README.md                       # This file
├── build.sh                        # Script for production builds (collectstatic, migrations)
├── manage.py                       # Django's command-line utility
└── requirements.txt                # List of all Python package dependencies
```

-----

## 🔐 Security Features

  * Built-in CSRF protection and secure password hashing.
  * Email verification for new user accounts.
  * Google reCAPTCHA v2 to prevent bot abuse.
  * Protection against XSS and SQL injection via Django's core features.
  * HTTPS is enforced in production environments.

-----

## 👨‍💻 Developer & Support

  * **Nwokike Onyeka**
  * **GitHub**: [@nwokike](https://github.com/nwokike)
  * **Email**: nwokikeonyeka@gmail.com

For support, use the **AI Support Chatbot** available 24/7 in the app or reach out via the contact form in the footer.

-----

**© 2025 Kiri.ng - Empowering Nigerian Artisans** 🇳🇬
