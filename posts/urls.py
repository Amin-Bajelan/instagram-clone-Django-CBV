from django.urls import path
from . import views

urlpatterns = [
    # url main page posts and set comment for posts
    path('index/', views.IndexView.as_view(), name='index_post'),
    # url to see posts is not private
    path('explore/', views.ExploreView.as_view(), name='explore_post'),
    # url to set up system like
    path('like/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
    # url see list of user liking post
    path('list-likes/<int:post_id>/', views.ListLikesView.as_view(), name='likes_list'),
    # url to see list comment for post
    path('comment/<int:post_id>/', views.ListCommentView.as_view(), name='list_comment'),
    # url to see list comment for delete
    path('comment/delete/<int:post_id>/', views.ListCommentDeleteView.as_view(), name='list_comment_delete'),
    #url to show list comment for delete
    path('comment/<int:pk>/remove/', views.DeleteCommentView.as_view(), name='delete_comment')
]