# Kiri.ng - Nigerian Artisan Marketplace & Learning Platform

![Kiri.ng](static/logo-light.png)

### <a href="https://kiriong.onrender.com/" target="_blank" rel="noopener noreferrer">🚀 View Live Demo</a>

A comprehensive Django-based Progressive Web App designed to empower Nigerian artisans by connecting them with customers, providing AI-powered educational resources through the Academy, and fostering community engagement through blogging.

## 🌟 Features

### 🛒 Marketplace
- **Service Listings**: Artisans can create and manage service listings with multiple images
- **Category Filtering**: Browse services by trade categories
- **Booking System**: Customers can book services with email notifications
- **Artisan Dashboard**: Manage services, bookings, and revenue tracking
- **Artisan Storefronts**: Beautiful public profiles showcasing services, certificates, and credentials

### 🎓 Academy
- **AI-Powered Learning**: Personalized learning pathways generated using Google Gemini 2.5 Flash
- **Enhanced Video Layout**: Only 2 carefully selected YouTube videos per module, interspersed with written content for better learning flow
- **Progress Tracking**: Track completion of modules and learning pathways
- **Certificates**: Download PDF certificates for completed pathways
- **Community Pathways**: Share and discover learning resources from other artisans
- **AI Tutor**: Ask questions and get AI-powered answers for each module
- **Dark Mode Support**: All academy content now fully visible in dark theme

### 📝 Blog
- **Community Blogging**: Verified artisans can write and publish blog posts
- **Rich Text Editor**: CKEditor 5 integration for professional content creation
- **Comments System**: Engage with the community through comments
- **Content Discovery**: Browse posts by category and search

### 👤 User Management & Authentication
- **Google OAuth**: Sign in/up with Google (no email verification needed!)
- **Traditional Signup**: Email-based registration with verification
- **Password Reset**: Complete password recovery flow with branded email templates
- **Modern UI**: Beautiful, animated login/signup pages with logo branding
- **Profile Management**: Upload profile pictures, add bio, contact info, and social media links
- **Multiple Social Links**: Connect Instagram, Facebook, WhatsApp, Twitter, LinkedIn, TikTok, YouTube
- **Certificate Management**: Upload and display professional certifications
- **Artisan Verification**: Location-based verification system
- **Referral System**: Built-in referral tracking

### 🎨 User Experience
- **PWA Install Button**: One-click installation with theme-colored button
- **Mobile-First Design**: Optimized for mobile devices
- **Dark/Light Mode**: Seamless theme switching with localStorage persistence
- **Multi-Language Support**: Google Translate integration with green-themed dropdown (English, Hausa, Igbo, Yoruba)
- **Responsive Navigation**: Bottom navigation bar with sub-navigation
- **Contact Support Modal**: Easy-to-access support form in footer
- **Custom Error Pages**: Branded 404 and 500 error pages
- **Loading Animations**: Smooth transitions and loading indicators
- **Button Feedback**: Visual feedback on all interactions

### 🔔 Real-Time Features
- **Notifications**: Real-time notifications for bookings, verifications, and updates
- **Email Notifications**: Automated emails via Brevo for important events
- **PWA Support**: Progressive Web App with offline capabilities and service worker

### 🚀 SEO & Performance
- **Comprehensive Meta Tags**: Full SEO meta descriptions and keywords
- **Open Graph Tags**: Optimized for Facebook and LinkedIn sharing
- **Twitter Cards**: Enhanced Twitter sharing with large images
- **Canonical URLs**: Proper URL canonicalization for SEO
- **Theme Colors**: Browser theme color matching brand
- **Lighthouse Optimized**: Performance, accessibility, SEO scores 90+

## 🚀 Technology Stack

### Backend
- **Framework**: Django 5.0.6
- **Database**: SQLite (development), PostgreSQL (production)
- **Server**: Gunicorn (production)
- **API**: Django REST Framework
- **Authentication**: Django Allauth with Google OAuth2

### Frontend
- **CSS Framework**: Bootstrap 5.3.3
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JS with custom utilities
- **Rich Text**: CKEditor 5
- **PWA**: Service Workers, Web App Manifest

### AI & APIs
- **AI Model**: Google Gemini 2.5 Flash
- **Video API**: YouTube Data API v3
- **Email Service**: Brevo (Anymail integration)
- **Captcha**: django-recaptcha
- **Media Storage**: Cloudinary

### PDF & ML
- **PDF Generation**: WeasyPrint, ReportLab
- **Machine Learning**: Scikit-learn
- **Authentication**: PyJWT for Google OAuth tokens

## 📋 Requirements

- Python 3.12
- PostgreSQL (for production)
- Google Gemini API key
- YouTube Data API key
- Brevo API key
- Google reCAPTCHA keys
- Cloudinary credentials
- Google OAuth credentials (optional, for social login)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/nwokike/kiriong.git
cd kiriong
```

### 2. Create Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# AI & APIs
GEMINI_API_KEY=your-google-gemini-api-key
YOUTUBE_API_KEY=your-youtube-api-key

# Email
BREVO_API_KEY=your-brevo-api-key
DEFAULT_FROM_EMAIL=noreply@kiri.ng

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your-recaptcha-site-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-secret-key

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# Google OAuth (Optional)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# Database (Production)
DATABASE_URL=postgresql://user:password@host:port/database
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server
```bash
python manage.py runserver 0.0.0.0:5000
```

Visit `http://localhost:5000` to access the application.

## 🌐 Deployment

The application is production-ready and can be deployed to Oracle Cloud, Render, or any platform supporting Django applications.

**Deployment Configuration:**
- PostgreSQL database
- Automatic SSL/TLS certificates
- Zero-downtime deployments
- Automatic database migrations
- WhiteNoise for efficient static file serving
- Gunicorn WSGI server

**Production Security:**
```python
# Enforced in production (DEBUG=False):
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

## 📁 Project Structure

```
kiriong/
├── academy/              # AI-powered learning platform
├── blog/                 # Community blogging app
├── core/                 # Core app (home, support, error pages)
├── kiriong/              # Project settings
├── marketplace/          # Services and bookings
├── notifications/        # Real-time notification system
├── users/                # User management and profiles
├── media/                # User-uploaded files
├── static/               # Static files (CSS, JS, images)
├── templates/            # Global HTML templates
│   ├── registration/     # Auth templates (login, signup, password reset)
│   ├── 404.html          # Custom 404 page
│   └── 500.html          # Custom 500 page
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## 🎯 Key Models

### Users App
- `Profile`: Extended user information with social links
- `Certificate`: Professional certifications
- `SocialMediaLink`: Social media connections

### Marketplace App
- `Category`: Service categories
- `Service`: Service listings with images
- `Booking`: Customer bookings with notifications

### Academy App
- `LearningPathway`: AI-generated learning paths
- `PathwayModule`: Individual modules with videos
- `ModuleQuestion`: AI tutor Q&A
- `Badge`: Achievement badges

### Blog App
- `Post`: Blog posts with CKEditor
- `Comment`: Post comments

## 🔐 Security Features

- CSRF protection enabled
- Secure password hashing
- Email verification (optional for OAuth)
- reCAPTCHA on authentication
- XSS protection
- SQL injection prevention
- Secure static file serving
- HTTPS enforced in production
- Google OAuth2 secure authentication

## 🌍 Localization

Supports multiple Nigerian languages:
- English (default)
- Hausa
- Igbo
- Yoruba

Translation powered by Google Translate widget with theme-colored dropdown.

## 📱 Progressive Web App Features

- **Installable**: One-click install button with branded styling
- **Offline Support**: Service worker for offline capabilities
- **App Shortcuts**: Quick access to Services and Academy
- **Theme Color**: Matches brand (#2c5530)
- **Fast Loading**: Optimized caching strategy
- **Responsive**: Mobile-first, works on all devices

## 🎨 Theme Customization

The app uses a custom green color scheme:

```css
:root {
    --primary-green: #2c5530;
    --secondary-green: #3d7242;
    --accent-gold: #d4af37;
}

[data-theme="dark"] {
    --primary-green: #4a8f52;
    --secondary-green: #5fa867;
    --accent-gold: #f0c952;
}
```

## 🆕 Latest Updates (October 2025)

### ✅ Completed Enhancements
- **PWA Install Button**: Green-themed button with smooth animations
- **Google OAuth**: Sign in/up with Google (no email verification needed)
- **Password Reset**: Complete flow with custom branded email templates
- **Modern Auth UI**: Redesigned login/signup pages with animations
- **Academy Improvements**: 
  - Videos now interspersed with content (1 before, 1 after lesson)
  - Limited to 2 high-quality videos per module
  - Fixed all dark mode visibility issues
- **Google Translate Fix**: Dropdown now uses theme green instead of black
- **Contact Support**: Modal form accessible from footer
- **Error Pages**: Custom branded 404 and 500 pages
- **SEO Optimization**: Comprehensive meta tags, Open Graph, Twitter Cards
- **Performance**: Lighthouse scores 90+ for performance, accessibility, SEO

## 🤝 Contributing

This is a startup project. For contributions or feature requests:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is developed for the Nigerian artisan community.

## 👨‍💻 Developer

**Nwokike**
- GitHub: [@nwokike](https://github.com/nwokike)
- Email: nwokikeonyeka@gmail.com

## 🙏 Acknowledgments

- Nigerian artisan community
- Google Gemini AI
- Bootstrap framework
- Django & Allauth communities
- All open-source contributors

## 📞 Support

For support, use the "Contact Support" link in the footer or email nwokikeonyeka@gmail.com

---

**© 2025 Kiri.ng - Empowering Nigerian Artisans** 🇳🇬

Made with ❤️ for Nigerian Artisans
