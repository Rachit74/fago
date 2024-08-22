from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.explore, name='explore-communities'),
    path('create_com/', views.create_community, name='create-community'),
    path('com/<int:community_id>', views.community, name='community'),
    path('join_com/<int:community_id>', views.join_community, name='join-community'),
    path('leave_com/<int:community_id>', views.leave_community, name='leave-community'),
    path('delete_com/<int:community_id>', views.delete_community, name='delete-community'),
]