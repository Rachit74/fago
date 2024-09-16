from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.get_posts, name='get_posts_endpoint'),
    path('login/', view=views.LoginView.as_view(), name='api_login_endpoint'),
    path('posts/<int:id>/', view=views.PostDetailView.as_view(), name='post_endpoint'),
]