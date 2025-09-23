from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('dashboard/', views.AcademyDashboardView.as_view(), name='dashboard'),
    path('', views.PathwayListView.as_view(), name='pathway-list'),
    path('create/', views.CreatePathwayView.as_view(), name='create-pathway'),
    
    # This is the original, private view for the owner
    path('pathway/<int:pk>/', views.PathwayDetailView.as_view(), name='pathway-detail'),

    # --- THIS IS THE NEW PUBLIC URL ---
    path('pathway/public/<int:pk>/<slug:slug>/', 
         views.PublicPathwayDetailView.as_view(), 
         name='public-pathway-detail'),
    
    path('module/<int:module_id>/complete/', views.complete_module, name='complete-module'),
]