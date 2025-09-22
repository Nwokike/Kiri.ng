from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.PathwayListView.as_view(), name='pathway-list'),
    path('create/', views.CreatePathwayView.as_view(), name='create-pathway'),
    path('pathway/<int:pk>/', views.PathwayDetailView.as_view(), name='pathway-detail'),
    path('module/<int:module_id>/complete/', views.complete_module, name='complete-module'),
]