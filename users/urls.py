from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile-detail'),
    path('profile/edit/', views.profile_edit_view, name='profile-edit'),
    path('verify-location/', views.verify_location_view, name='verify-location'),
]