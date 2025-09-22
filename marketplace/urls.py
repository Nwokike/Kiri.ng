from django.urls import path
from .views import (
    ServiceListView, 
    ServiceDetailView, 
    ServiceCreateView, 
    ArtisanDashboardView,
    ServiceUpdateView, 
    ServiceDeleteView, 
)

app_name = 'marketplace'

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/new/', ServiceCreateView.as_view(), name='service-create'),
    path('dashboard/', ArtisanDashboardView.as_view(), name='artisan-dashboard'),
    path('dashboard/service/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service-update'),
    path('dashboard/service/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
]