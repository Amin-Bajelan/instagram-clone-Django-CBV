from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index_post'),
    path('explore/', views.ExploreView.as_view(), name='explore_post'),
    path('like/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
    path('list-likes/<int:post_id>', views.ListLikesView.as_view(), name='likes_list'),
]