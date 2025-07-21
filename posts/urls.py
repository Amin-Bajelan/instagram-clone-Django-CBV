from django.urls import path
from . import views

urlpatterns = [
    # url main page posts and set comment for posts
    path('index/', views.IndexView.as_view(), name='index_post'),
    # url add new post
    path('add-post/', views.AddPostView.as_view(), name='add_post'),
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
    # url to show list comment for delete
    path('comment/<int:pk>/remove/', views.DeleteCommentView.as_view(), name='delete_comment'),
    # url delete posts for login user
    path("delete/post/<int:pk>/", views.DeletePostView.as_view(), name='delete_post'),
    # url for edit posts for login user
    path('edit/<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    # url to search username
    path('search/', views.SearchView.as_view(), name='search_post'),
    # url send follow request and message for user
    path('send/follow/<int:pk>/', views.FollowRequestView.as_view(), name='follow_request'),
    # url accept follow request
    path('accept/follow/<int:pk>/', views.AcceptFollowView.as_view(), name='accept_follow'),
    # url unfollow
    path('unfollow/<int:pk>/', views.UnfollowRequestView.as_view(), name='unfollow'),
    # url delete notification
    path('cancel/notification/<int:pk>/', views.CancelNotificationView.as_view(), name='cancel_follow_request'),
    # url see list my notification
    path('show/notifications/', views.ShowNotificationsView.as_view(), name='show_notifications'),
    # url show my list comments
    path('show/my/comments/<int:pk>/', views.ShowMyCommentsView.as_view(), name='show_my_comments'),
    # url delete my account comments
    path('delete/comment/<int:pk>/', views.DeleteMyCommentView.as_view(), name='delete_my_comment'),
    # url show list follower
    path('show/follower/<int:pk>', views.ShowMyFollower.as_view(), name='show_follower'),
    # url show list following
    path('show/following/<int:pk>', views.ShowFollowingView.as_view(), name='show_following'),
    # delete follower
    path('delete/follower/<int:pk>/', views.DeleteFollowerView.as_view(), name='delete_follower'),
    # url delete following
    path('delete/following/<int:pk>', views.DeleteFollowingView.as_view(), name='delete_following'),

]