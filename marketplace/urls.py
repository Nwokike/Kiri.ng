from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # --- THIS IS THE FIX: New patterns for filtering ---
    path('', views.ServiceListView.as_view(), name='service-list'), # Changed from 'services/'
    path('category/<slug:category_slug>/', views.ServiceListView.as_view(), name='service-list-by-category'),
    
    path('service/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'), # Changed from 'services/'
    path('dashboard/', views.ArtisanDashboardView.as_view(), name='artisan-dashboard'),
    path('dashboard/service/new/', views.ServiceCreateView.as_view(), name='service-create'),
    path('dashboard/service/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service-update'),
    path('dashboard/service/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service-delete'),
]