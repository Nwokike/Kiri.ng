from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'), # <-- Add this line
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
]