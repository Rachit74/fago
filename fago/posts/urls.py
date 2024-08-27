from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('read/<int:post_id>', views.ReadPostView.as_view(), name='read-post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete-post'),
    path('delete_comment/<int:comment_id>',views.delete_comment, name='delete-comment'),
    path('comment_reply/<int:comment_id>', views.CommentReplyView.as_view(), name='comment-reply'),
    path('create_post/', views.CreatePostView.as_view(), name='create-post'),

    path('delete_notification/<int:notification_id>', views.delete_notification, name='delete-notification'),
    path('notification/<int:notification_id>', views.notification, name='notification'),

    path('search/', views.search, name='search'),
]