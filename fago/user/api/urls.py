from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UsersView.as_view()),
    path('users/<int:id>/', views.UserEndpoint.as_view()),
    path('users/register/', views.RegisterUsersView.as_view()),
]