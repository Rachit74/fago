from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('read/<int:post_id>', views.read_post, name='read-post'),
    path('create_post/', views.create_post, name='create-post'),
]