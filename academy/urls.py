from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.AcademyHomeView.as_view(), name='home'),
    path('dashboard/', views.AcademyDashboardView.as_view(), name='dashboard'),
    path('pathways/', views.PathwayListView.as_view(), name='pathway-list'),
    path('create/', views.CreatePathwayView.as_view(), name='create-pathway'),
    path('pathway/<int:pk>/', views.PathwayDetailView.as_view(), name='pathway-detail'),
    path(
        'pathway/public/<int:pk>/<slug:slug>/',
        views.PublicPathwayDetailView.as_view(),
        name='public-pathway-detail',
    ),
    path('module/<int:module_id>/complete/', views.complete_module, name='complete-module'),
    path('module/<int:module_id>/ask-question/', views.ask_question, name='ask-question'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    path(
        'pathway/<int:pk>/download-certificate/',
        views.DownloadCertificateView.as_view(),
        name='download-certificate',
    ),
]
