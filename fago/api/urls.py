from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.get_posts, name='get_posts_endpoint'),
    path('posts/<int:id>/', views.get_post, name='get_post_endpoint'),
]