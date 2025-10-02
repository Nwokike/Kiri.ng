# Deployment Guide - Render

## Quick Deployment (3 Steps)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com and sign up (100% free)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account
4. Find and select your repository
5. Click **"Apply"**

Render will automatically:
- ✅ Create a free PostgreSQL database
- ✅ Generate a secure SECRET_KEY
- ✅ Run migrations
- ✅ Collect static files
- ✅ Deploy your app

### Step 3: Add Environment Variables (Optional)

After deployment, add API keys in **Environment** settings:

| Variable Name | Get It Here | Purpose |
|--------------|-------------|---------|
| `GEMINI_API_KEY` | https://aistudio.google.com/app/apikey | AI-powered learning features |
| `YOUTUBE_API_KEY` | https://console.cloud.google.com/apis/credentials | Video content integration |
| `BREVO_API_KEY` | https://app.brevo.com/settings/keys/api | Email notifications |
| `DEFAULT_FROM_EMAIL` | Your email address | Sender email |
| `RECAPTCHA_PUBLIC_KEY` | https://www.google.com/recaptcha/admin | Anti-spam protection |
| `RECAPTCHA_PRIVATE_KEY` | https://www.google.com/recaptcha/admin | Anti-spam protection |

**Note:** The app works without these, but some features require them.

---

## Getting Your API Keys

### GEMINI_API_KEY (AI Academy)
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click **"Create API Key"**
4. Copy and paste into Render environment variables

### YOUTUBE_API_KEY (Video Integration)
1. Visit: https://console.cloud.google.com/apis/credentials
2. Click **"Create Credentials"** → **"API Key"**
3. Enable **"YouTube Data API v3"** for your project
4. Copy and paste into Render environment variables

### BREVO_API_KEY (Email Service)
1. Visit: https://app.brevo.com (free account)
2. Go to **Settings** → **API Keys**
3. Click **"Generate a new API Key"**
4. Copy and paste into Render environment variables

### RECAPTCHA Keys (Anti-Spam)
1. Visit: https://www.google.com/recaptcha/admin
2. Register a new site with **reCAPTCHA v2** → **"I'm not a robot" Checkbox**
3. Add your domain (e.g., `kiri.onrender.com`)
4. Copy both **Site Key** (public) and **Secret Key** (private)
5. Add both to Render environment variables

---

## 100% Free Deployment

**Everything is FREE:**
- ✅ Render free tier (750 hours/month)
- ✅ PostgreSQL database (free tier - 1GB storage)
- ✅ Google Gemini API (free tier)
- ✅ YouTube Data API (free tier)
- ✅ Brevo email (free tier - 300 emails/day)
- ✅ Google reCAPTCHA (100% free)
- ✅ SSL certificate (included free)

**Your live URL:** `https://kiri.onrender.com`

---

## Database Configuration

The app automatically switches databases:
- **Development:** SQLite (`db.sqlite3`)
- **Production:** PostgreSQL (via `DATABASE_URL`)

No code changes needed!

---

## Troubleshooting

**Build fails?**
- Check that `build.sh` is executable: `chmod +x build.sh`
- Verify all dependencies are in `requirements.txt`

**Database errors?**
- Wait a few minutes for PostgreSQL to provision
- Check that `DATABASE_URL` is set in environment variables

**Static files missing?**
- Render runs `python manage.py collectstatic` automatically via `build.sh`
- Check build logs for any errors

**App not loading?**
- Check that `DEBUG=False` in environment variables
- Verify gunicorn is in `requirements.txt`

---

## After Deployment

1. Visit your live site: `https://kiri.onrender.com`
2. Create admin account via Render Shell:
   ```bash
   python manage.py createsuperuser
   ```
3. Access admin panel: `https://kiri.onrender.com/admin`
