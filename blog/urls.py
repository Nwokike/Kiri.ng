from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('edit/<int:pk>/', views.PostUpdateView.as_view(), name='post_edit'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]