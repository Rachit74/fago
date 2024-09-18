from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('edit_profile/', views.edit_user_profile, name='edit-profile'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
]