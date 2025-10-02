from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
]