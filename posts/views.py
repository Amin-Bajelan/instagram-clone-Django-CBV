from django.utils import timezone

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# models
from accounts.models import User, Profile
from posts.models import Post, Follow, Notification, Comment

from .forms import CommentForm


# Create your views here.

class IndexView(TemplateView, LoginRequiredMixin):
    """
    main page for instagram clone to show posts and profile and edite profile
    """
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        follower_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        context['posts'] = Post.objects.filter(user__in=follower_ids).order_by('-date_posted')
        return context

    """
    ability send comment 
    """

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            post_id = request.POST.get('post_id')
            comment.post = Post.objects.get(id=post_id)
            post = Post.objects.get(id=post_id)
            post.num_comments += 1
            post.save()
            comment.save()
        return redirect('index_post')


class AddPostView(CreateView, LoginRequiredMixin):
    """
    a view for adding new by user post
    """
    model = Post
    fields = ['image', 'caption']
    template_name = 'posts/add_post.html'
    success_url = '/show_profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        user_1 = Profile.objects.get(user=self.request.user)
        user_1.post_count += 1
        user_1.save()
        return super().form_valid(form)


class ExploreView(View, LoginRequiredMixin):
    """
    a view for explor filter following and not private account
    """
    def get(self, request):
        user = request.user
        public_users = Profile.objects.filter(is_private=False).values_list('user', flat=True)
        post_1 = Post.objects.filter(user__in=public_users)
        followings = Follow.objects.filter(follower=user).values_list('following', flat=True)
        post_2 = Post.objects.filter(user__in=followings)
        combined = list(post_1) + list(post_2)
        unique_posts = {post.id: post for post in combined}.values()
        return render(request, 'posts/explore.html', {'posts': unique_posts})


class LikePostView(View, LoginRequiredMixin):
    """
    a view to handle liking posts
    """

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if user in post.liked_by.all():
            post.liked_by.remove(user)
            post.likes -= 1
        else:
            post.liked_by.add(user)
            post.likes += 1
        notification = Notification.objects.create(
            to_user=post.user,
            from_user=request.user,
            notification_type='like',
            post=post,
            date_created=timezone.now()
        )
        notification.save()
        post.save()
        return redirect('/posts/index/')


class ListLikesView(ListView, LoginRequiredMixin):
    """
    a view to see list of person liking posts
    """
    template_name = 'posts/likes_list.html'
    context_object_name = 'liked_users'
    model = Post

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        return post.liked_by.all()


class ListCommentView(ListView, LoginRequiredMixin):
    """
    view to see list of post comments
    """
    template_name = 'posts/list_comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        return comments


class ListCommentDeleteView(ListView, LoginRequiredMixin):
    """
    view to see list of post comments for delete
    """
    template_name = 'posts/list_comments_delete.html'
    context_object_name = 'comments'

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        return comments


class DeleteCommentView(View, LoginRequiredMixin):
    """
    a simple view to delete a post comment
    """

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.user == request.user:
            post = comment.post
            comment.delete()
            if post.num_comments > 0:
                post.num_comments -= 1
                post.save()
        return redirect('show_profile')


class DeletePostView(DeleteView, LoginRequiredMixin):
    """
    a view to delete a post
    """
    model = Post
    success_url = reverse_lazy('show_profile')


class EditPostView(UpdateView, LoginRequiredMixin):
    """
    a view to edit a post
    """
    model = Post
    fields = ['caption']
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy('show_profile')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class SearchView(View, LoginRequiredMixin):
    """
    View to search username
    """

    def post(self, request):
        input_search = request.POST.get('input_search', '').strip()
        profile = Profile.objects.filter(user_name__icontains=input_search)
        return render(request, 'posts/search_result.html', {'profile': profile})


class FollowRequestView(View, LoginRequiredMixin):
    """
    a view for create notification follow request
    """

    def post(self, request, pk):
        user_receiver = get_object_or_404(User, pk=pk)
        user_sender = request.user

        notification, created = Notification.objects.get_or_create(
            notification_type='follow',
            from_user=user_sender,
            to_user=user_receiver,
            date_created=timezone.now()
        )

        return redirect(reverse('show_profile_user', args=[user_receiver.id]))


class AcceptFollowView(View, LoginRequiredMixin):
    """
    a view to accept a follow request
    """

    def post(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        notification.is_read = True
        accept_follow = Follow.objects.create(
            follower=notification.from_user,
            following=notification.to_user,
            date_followed=timezone.now()
        )
        obj1 = Profile.objects.get(user=notification.to_user)
        obj1.followers += 1
        obj2 = Profile.objects.get(user=notification.from_user)
        obj2.following += 1
        notification.delete()

        accept_follow.save()
        obj1.save()
        obj2.save()
        return redirect('/posts/index/')


class UnfollowRequestView(View, LoginRequiredMixin):
    """
    a view to unfollow user
    """

    def post(self, request, pk):
        follow = Follow.objects.get(follower=request.user, following=User.objects.get(pk=pk))
        profile_1 = Profile.objects.get(user=User.objects.get(pk=pk))
        profile_1.followers -= 1
        profile_2 = Profile.objects.get(user=request.user)
        profile_2.following -= 1
        profile_1.save()
        profile_2.save()
        follow.delete()
        return redirect(reverse('show_profile_user', args=[pk]))


class CancelNotificationView(View, LoginRequiredMixin):
    def post(self, request, pk):
        receiver = get_object_or_404(User, pk=pk)
        Notification.objects.filter(
            to_user=receiver,
            from_user=request.user,
            notification_type='follow'
        ).delete()
        return redirect(reverse('show_profile_user', args=[pk]))


class ShowNotificationsView(View, LoginRequiredMixin):
    """
    view to show notifications
    """

    def post(self, request):
        notifications = Notification.objects.filter(to_user=request.user)
        return render(request, 'posts/show_notifications.html', {'notifications': notifications})


class ShowMyCommentsView(View, LoginRequiredMixin):
    """
    Show all comments related to a specific post for the current user
    """

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post, user=request.user)  # یا فقط post=post
        return render(request, 'posts/show_my_comments.html', {'comments': comments})


class DeleteMyCommentView(View, LoginRequiredMixin):
    """
    Delete comment my posts
    """

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        post = Post.objects.get(id=comment.post.id)
        post_id = post.id
        post.num_comments -= 1
        comment.delete()
        post.save()
        return redirect('show_profile')


class ShowMyFollower(View, LoginRequiredMixin):
    """
    a view to show my follower profile and delete them
    """

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        follower = Follow.objects.filter(following=user)
        return render(request, 'posts/user_follower.html', {'follow': follower})


class ShowFollowingView(View, LoginRequiredMixin):
    """
    a view to show my following profile and delete them
    """

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        follower = Follow.objects.filter(follower=user)
        return render(request, 'posts/user_following.html', {'follow': follower})


class DeleteFollowerView(View, LoginRequiredMixin):
    """
    view for delete follower
    """

    def post(self, request, pk):
        following = Follow.objects.filter(following=request.user, follower=User.objects.get(pk=pk))
        profile_1 = Profile.objects.get(user=request.user)
        profile_1.followers -= 1
        profile_1.save()
        profile_2 = Profile.objects.get(user=User.objects.get(pk=pk))
        profile_2.following -= 1
        profile_2.save()
        following.delete()
        return redirect('show_profile')


class DeleteFollowingView(View, LoginRequiredMixin):
    """
    view for delete following
    """

    def post(self, request, pk):
        follower = Follow.objects.filter(follower=request.user, following=User.objects.get(pk=pk))
        profile_1 = Profile.objects.get(user=request.user)
        profile_1.following -= 1
        profile_1.save()
        profile_2 = Profile.objects.get(user=User.objects.get(pk=pk))
        profile_2.followers -= 1
        profile_2.save()
        follower.delete()
        return redirect('show_profile')
