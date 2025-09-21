from django.urls import path
from .views import AcademyDashboardView, PathwayDetailView, complete_module

app_name = 'academy'

urlpatterns = [
    path('academy/', AcademyDashboardView.as_view(), name='dashboard'),
    path('academy/pathway/<int:pk>/', PathwayDetailView.as_view(), name='pathway-detail'),
    path('academy/module/<int:module_id>/complete/', complete_module, name='complete-module'),
]