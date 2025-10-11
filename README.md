# Kiri.ng - Nigerian Artisan Marketplace & Learning Platform

![Kiri.ng Logo](static/logo-light.png)

## 🚀 [Live Site](https://kiri.ng/)

A comprehensive Django PWA connecting Nigerian artisans with customers, featuring AI-powered learning pathways and community engagement.

## ✨ Key Features

### 🛒 Marketplace
- Service listings with booking system
- ML-based service recommendations
- Artisan dashboards and storefronts
- Automated email notifications

### 🎓 Academy
- AI-powered personalized learning pathways (Google Gemini 2.5 Flash)
- Progress tracking and certificates
- PDF certificate download
- AI Tutor for module questions
- Community pathway sharing

### 🤖 AI Customer Service
- 24/7 intelligent support chatbot
- Task-specific help guides
- Admin control capabilities
- Powered by Google Gemini AI

### 📝 Blog
- Community blogging with CKEditor 5
- Comments and engagement
- Content discovery

### 🔔 Real-Time Features
- Push notifications (Web Push API - works on all platforms except iOS)
- In-app notifications
- Email notifications (Brevo)
- PWA with offline capabilities

### 🎨 User Experience
- Progressive Web App (PWA)
- Dark/Light mode toggle
- Mobile-first responsive design
- Multi-language support (English, Hausa, Igbo, Yoruba)
- Google Analytics & AdSense integration

### 👤 User Features
- Google OAuth & traditional signup
- Profile management with social links
- Certificate uploads
- Referral system with URL tracking
- Location verification

## 🛠 Tech Stack

**Backend:** Django 5.0.6, PostgreSQL, Gunicorn  
**Frontend:** Bootstrap 5.3.3, Vanilla JS, CKEditor 5  
**AI & APIs:** Google Gemini 2.5 Flash, YouTube Data API v3  
**Services:** Brevo (email), Cloudinary (media), Google OAuth  
**ML:** Scikit-learn (service recommendations)  
**PDF:** WeasyPrint, ReportLab

## 📋 Requirements

- Python 3.12
- PostgreSQL
- API Keys (see Environment Variables)

## 🚀 Quick Setup

### 1. Clone & Install
```bash
git clone https://github.com/nwokike/kiri.ng.git
cd kiri.ng
pip install -r requirements.txt
```

### 2. Environment Variables
Create `.env` file:
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

# Media
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Google OAuth (optional)
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# reCAPTCHA (optional)
RECAPTCHA_PUBLIC_KEY=your-site-key
RECAPTCHA_PRIVATE_KEY=your-secret-key

# Analytics & Ads
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
GOOGLE_ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXX
```

### 3. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 4. Run Development Server
```bash
python manage.py runserver 0.0.0.0:5000
```

Visit `http://localhost:5000`

## 🌐 Deployment

**Production Ready Features:**
- PostgreSQL database
- Automatic SSL/TLS
- Zero-downtime deployments
- WhiteNoise for static files
- Gunicorn WSGI server
- Secure cookies and HTTPS enforced

**Build Command:**
```bash
./build.sh
```

## 📁 Project Structure

```
kiri.ng/
├── academy/          # AI-powered learning platform
├── blog/             # Community blogging
├── core/             # Core app + AI customer service
├── marketplace/      # Services and bookings
├── notifications/    # Notification system
├── users/            # User management and profiles
├── static/           # Static files (CSS, JS, images)
├── templates/        # Global templates
└── media/            # User-uploaded files
```

## 🔐 Security Features

- CSRF protection
- Secure password hashing
- Email verification
- reCAPTCHA integration
- XSS & SQL injection prevention
- HTTPS enforced in production

## 📱 PWA Features

- Installable on all devices
- Offline support via service worker
- Push notifications
- App shortcuts
- Fast loading with caching

## 👨‍💻 Developer

**Nwokike**  
- GitHub: [@nwokike](https://github.com/nwokike)
- Email: nwokikeonyeka@gmail.com

## 📞 Support

- AI Support: Available 24/7 in-app
- Email: nwokikeonyeka@gmail.com
- Contact form: Available in footer

---

**© 2025 Kiri.ng - Empowering Nigerian Artisans** 🇳🇬
