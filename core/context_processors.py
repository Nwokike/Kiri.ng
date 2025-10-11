from django.conf import settings
from notifications.models import Notification

def google_analytics(request):
    return {
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'GOOGLE_ADSENSE_CLIENT_ID': settings.GOOGLE_ADSENSE_CLIENT_ID,
    }

# --- THIS IS THE NEW FUNCTION ---
def notifications(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        return {
            'unread_notifications': unread_notifications,
            'unread_notification_count': unread_notifications.count(),
        }
    return {}