from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('edit_profile/', views.edit_user_profile, name='edit-profile')
]