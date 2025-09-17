from django.urls import path
from .views import ServiceListView, ServiceDetailView, ServiceCreateView

app_name = 'marketplace'

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/new/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]