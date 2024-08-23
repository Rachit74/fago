from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('read/<int:post_id>', views.read_post, name='read-post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete-post'),
    path('delete_comment/<int:comment_id>',views.delete_comment, name='delete-comment'),
    path('create_post/', views.create_post, name='create-post'),
]