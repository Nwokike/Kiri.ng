from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Replace the old LogoutView with our new logout_view function
    path('logout/', views.logout_view, name='logout'),
]