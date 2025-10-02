# Kiri.ng - Empowering Nigerian Artisans

![Kiri.ng](static/logo-light.png)

A comprehensive Django-based platform designed to empower Nigerian artisans by connecting them with customers, providing educational resources through the Academy, and fostering community engagement through blogging.

## 🌟 Features

### 🛒 Marketplace
- **Service Listings**: Artisans can create and manage service listings with multiple images
- **Category Filtering**: Browse services by trade categories
- **Booking System**: Customers can book services with email notifications
- **Artisan Dashboard**: Manage services, bookings, and revenue tracking
- **Artisan Storefronts**: Beautiful public profiles showcasing services, certificates, and credentials

### 🎓 Academy
- **AI-Powered Learning**: Personalized learning pathways generated using Google Gemini 2.5 Flash
- **Video Integration**: Curated YouTube videos for each module via YouTube Data API
- **Progress Tracking**: Track completion of modules and learning pathways
- **Certificates**: Download PDF certificates for completed pathways
- **Community Pathways**: Share and discover learning resources from other artisans
- **Badges & Achievements**: Earn badges for completing learning milestones

### 📝 Blog
- **Community Blogging**: Verified artisans can write and publish blog posts
- **Rich Text Editor**: CKEditor 5 integration for professional content creation
- **Comments System**: Engage with the community through comments
- **Content Discovery**: Browse posts by category and search

### 👤 User Management
- **Email Verification**: Secure account creation with email verification
- **Artisan Verification**: Location-based verification system with Google Maps integration
- **Profile Management**: Upload profile pictures, add bio, contact info, and social media links
- **Multiple Social Links**: Connect Instagram, Facebook, WhatsApp, Twitter, LinkedIn, TikTok, YouTube, and custom websites
- **Certificate Management**: Upload and display professional certifications
- **Referral System**: Built-in referral tracking

### 🔔 Real-Time Features
- **Notifications**: Real-time notifications for bookings, verifications, and updates
- **Email Notifications**: Automated emails via Brevo for important events
- **PWA Support**: Progressive Web App with offline capabilities

### 🎨 User Experience
- **Mobile-First Design**: Optimized for mobile devices
- **Dark/Light Mode**: Seamless theme switching with user preference persistence
- **Multi-Language Support**: Google Translate integration (English, Hausa, Igbo, Yoruba)
- **Responsive Navigation**: Bottom navigation bar with sub-navigation
- **Security**: Google reCAPTCHA protection on signup/login
- **Terms of Service**: Mandatory ToS acceptance during signup

## 🚀 Technology Stack

### Backend
- **Framework**: Django 5.0.6
- **Database**: SQLite (development), PostgreSQL (production)
- **Server**: Gunicorn (production)
- **API**: Django REST Framework

### Frontend
- **CSS Framework**: Bootstrap 5.3.3
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JS with custom utilities
- **Rich Text**: CKEditor 5

### AI & APIs
- **AI Model**: Google Gemini 2.5 Flash
- **Video API**: YouTube Data API v3
- **Email Service**: Brevo (Anymail integration)
- **Captcha**: django-recaptcha

### PDF & ML
- **PDF Generation**: WeasyPrint, ReportLab
- **Machine Learning**: Scikit-learn
- **NLP**: TensorFlow, Transformers

## 📋 Requirements

- Python 3.12
- PostgreSQL (for production)
- Google Gemini API key
- YouTube Data API key
- Brevo API key
- Google reCAPTCHA keys

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

## 🌐 Deployment (Render)

### Prerequisites
- Render account
- GitHub repository

### Steps

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Create New Web Service on Render**
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables**
   Set these in Render dashboard:
   - `GEMINI_API_KEY`
   - `YOUTUBE_API_KEY`
   - `BREVO_API_KEY`
   - `DEFAULT_FROM_EMAIL`
   - `RECAPTCHA_PUBLIC_KEY`
   - `RECAPTCHA_PRIVATE_KEY`

4. **Database**
   - Render will automatically create PostgreSQL database
   - Connection string is auto-configured

5. **Deploy**
   - Render will run `build.sh` automatically
   - Application will start with gunicorn

### Deployment Configuration

The project includes:
- `render.yaml`: Service configuration
- `build.sh`: Build script for migrations and static files
- Gunicorn WSGI server
- WhiteNoise for static file serving
- PostgreSQL with automatic connection

## 📁 Project Structure

```
kiriong/
├── academy/              # Learning platform app
├── blog/                 # Community blogging app
├── core/                 # Main app with home pages
├── kiriong/              # Project settings
├── marketplace/          # Services and bookings
├── notifications/        # Notification system
├── users/                # User management and profiles
├── media/                # User-uploaded files
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── build.sh              # Deployment build script
├── manage.py             # Django management script
├── render.yaml           # Render deployment config
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## 🎯 Key Models

### Users App
- `Profile`: Extended user information
- `Certificate`: Professional certifications
- `SocialMediaLink`: Social media connections

### Marketplace App
- `Category`: Service categories
- `Service`: Service listings
- `Booking`: Customer bookings

### Academy App
- `LearningPathway`: AI-generated learning paths
- `PathwayModule`: Individual modules
- `Badge`: Achievement badges

### Blog App
- `Post`: Blog posts
- `Comment`: Post comments

## 🔐 Security Features

- CSRF protection enabled
- Secure password hashing
- Email verification required
- reCAPTCHA on authentication
- XSS protection
- SQL injection prevention
- Secure static file serving
- HTTPS enforced in production

## 🌍 Localization

Supports multiple Nigerian languages:
- English (default)
- Hausa
- Igbo
- Yoruba

Translation powered by Google Translate widget.

## 📱 Progressive Web App

- Service worker for offline capabilities
- Installable on mobile devices
- Fast loading with caching
- Responsive design

## 🤝 Contributing

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

## 🙏 Acknowledgments

- Nigerian artisan community
- Google Gemini AI
- Bootstrap framework
- Django community
- All open-source contributors

## 📞 Support

For support, email support@kiri.ng or visit our community blog.

---

**© 2025 Kiri.ng - Empowering Nigerian Artisans**
