# Kiri.ng - Deployment Checklist

## Changes Made

### ✅ Phase 1: UI/UX Improvements
- **Login/Signup Forms**: Widened from `col-md-5` to `col-md-6 col-lg-5` for better desktop display
- **Academy Page**: Fixed mobile button spacing with `d-grid gap-2 d-md-flex` for signup/login buttons
- **Logo**: Removed drop-shadow filter and padding, reduced size to 60px for cleaner look
- **Dark Mode**: Changed to pure black (`#0a0a0a`) background for better eye comfort
- **Google Translate**: Changed color scheme to green (app's primary color `#2c5530`)

### ✅ Phase 2: Authentication & Security
- **CSRF Origins**: Updated to include `https://kiri.ng` and `https://www.kiri.ng`
- **Custom Adapters**: Implemented `CustomSocialAccountAdapter` and `CustomAccountAdapter` for:
  - Account linking (form users can login with Google)
  - Referral capture during Google OAuth signup
  - Email-based account connection
- **Password Reset**: Domain configured for kiri.ng (via Django Sites framework)

### ✅ Phase 3: Referral System Overhaul
- **New Field**: Added `referral_code` (unique, auto-generated UUID) to Profile model
- **Migration**: Created migration `0013_profile_referral_code.py` with data migration for existing users
- **URL-Based Referrals**: Implemented `?ref=CODE` parameter support
- **Session Handling**: Referral codes stored in session for Google OAuth signup
- **Dual Support**: Works for both form signup AND Google OAuth signup
- **Backward Compatible**: Still supports old username-based referral codes
- **Files Created**:
  - `users/signals.py` - Post-save signal for Profile creation
  - `users/adapters.py` - Custom allauth adapters
  - `users/management/commands/generate_referral_codes.py` - Management command

### ✅ Phase 4: PWA Enhancements
- **Theme Color**: Changed from blue (`#0d6efd`) to green (`#2c5530`) in manifest.json
- **Service Worker**: Verified URLs and scope are correct

### ✅ Phase 5: Academy Content
- **Timing Messages**:
  - "Generating pathway": Changed from "2 minutes" to "30 seconds"
  - "Submitting module": Changed from "1 minute" to "20 seconds"  
  - "Loading indicator": Changed from "10-15 seconds" to "up to 30 seconds"
- **Ask AI Form**: Removed `required` attribute (JavaScript not needed)

### ✅ Phase 6: Technical
- **Python Version**: Confirmed running on Python 3.12.11 ✓
- **Requirements**: All dependencies compatible

## Before Deploying to Production

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Django Site
```bash
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.get(id=1)
>>> site.domain = 'kiri.ng'
>>> site.name = 'Kiri.ng'
>>> site.save()
>>> exit()
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Generate Referral Codes for Existing Users (Optional)
```bash
python manage.py generate_referral_codes
```

### 5. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 6. Environment Variables Required
Make sure these are set in production:
- `SECRET_KEY`
- `DATABASE_URL`
- `GEMINI_API_KEY`
- `YOUTUBE_API_KEY`
- `BREVO_API_KEY`
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `RECAPTCHA_PUBLIC_KEY`
- `RECAPTCHA_PRIVATE_KEY`
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `DEFAULT_FROM_EMAIL`
- `DEBUG=False`

### 7. Test Critical Flows
1. **Form Signup with Referral Link**: Visit `/users/signup/?ref=TESTCODE`
2. **Google OAuth Signup with Referral**: Visit `/users/signup/?ref=TESTCODE` then click Google
3. **Account Linking**: Form user trying to login with Google (same email)
4. **Password Reset**: Both form and Google users
5. **Academy Timing**: Check loading messages display correctly
6. **PWA Install**: Verify green theme color on Android/iOS

## Known Limitations

### Push Notifications
Push notifications for PWA require:
- VAPID key generation
- Backend subscription endpoint
- Service worker updates for push event handling
- APNs configuration for iOS

This feature was marked as "not implemented" as it requires additional infrastructure setup. Recommend implementing this as a separate project phase with proper testing environment.

## Files Modified
- `templates/registration/login.html`
- `templates/registration/signup.html`
- `academy/templates/academy/academy_home.html`
- `academy/templates/academy/pathway_detail.html`
- `core/templates/core/base.html`
- `static/manifest.json`
- `static/css/custom.css`
- `static/js/custom.js`
- `kiriong/settings.py`
- `users/models.py`
- `users/views.py`
- `users/apps.py`

## Files Created
- `users/signals.py`
- `users/adapters.py`
- `users/management/commands/generate_referral_codes.py`
- `users/migrations/0013_profile_referral_code.py`

## Database Changes
- Added `referral_code` field to `Profile` model (CharField, unique, max_length=20)
- Added custom save method to auto-generate referral codes
- Data migration to populate existing users with referral codes

## Rollback Plan
If issues occur in production:
1. Revert to previous commit: `git revert HEAD`
2. Run: `python manage.py migrate users 0012_alter_socialmedialink_platform`
3. Restart application server

## Next Steps for User
After deployment, users should:
1. Share their referral link: `https://kiri.ng/users/signup/?ref=THEIR_CODE`
2. View their referral code in their profile (you may want to add UI for this)
3. Test all functionality thoroughly on production
