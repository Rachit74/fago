from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.ExploreView.as_view(), name='explore-communities'),
    path('create_com/', views.CreateCommunityView.as_view(), name='create-community'),
    path('<str:community>/', views.CommunityView.as_view(), name='community'),
    path('join_com/<str:community>', views.join_community, name='join-community'),
    path('leave_com/<str:community>', views.leave_community, name='leave-community'),
    path('delete_com/<str:community>', views.delete_community, name='delete-community'),

    path('pin/<int:post_id>', views.pin_post, name='pin'),
    path('unpin/<int:post_id>', views.unpin_post, name='unpin'),
]