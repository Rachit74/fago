from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.explore, name='explore-communities'),
    path('create_com/', views.create_community, name='create-community'),
    path('<str:community>', views.community, name='community'),
    path('join_com/<str:community>', views.join_community, name='join-community'),
    path('leave_com/<str:community>', views.leave_community, name='leave-community'),
    path('delete_com/<str:community>', views.delete_community, name='delete-community'),

    path('pin/<int:post_id>', views.pin_post, name='pin'),
    path('unpin/<int:post_id>', views.unpin_post, name='unpin'),
]