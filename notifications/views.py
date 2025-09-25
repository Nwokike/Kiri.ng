from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification

class NotificationListView(LoginRequiredMixin, generic.ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        # Mark all unread notifications as read when the user visits this page
        unread_notifications = Notification.objects.filter(recipient=self.request.user, is_read=False)
        unread_notifications.update(is_read=True)
        # Return all notifications for the user
        return Notification.objects.filter(recipient=self.request.user)