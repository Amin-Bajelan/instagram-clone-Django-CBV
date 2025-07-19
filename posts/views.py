from django.utils import timezone

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, DeleteView, UpdateView, CreateView
# models
from accounts.models import User, Profile
from posts.models import Post, Follow, Notification, Comment

from .forms import CommentForm


# Create your views here.

class IndexView(TemplateView):
    """
    main page for instagram clone to show posts and profile and edite profile
    """
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['posts'] = Post.objects.all()

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


class AddPostView(CreateView):
    """
    a view for adding new by user post
    """
    model = Post
    fields = ['image', 'caption']
    template_name = 'posts/add_post.html'
    success_url = '/show_profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExploreView(ListView):
    """
    a view to show all posts who's not private
    """
    model = Post
    template_name = 'posts/explore.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user__profile__is_private=False).order_by('-date_posted')


class LikePostView(View):
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

        post.save()
        return redirect('/posts/index/')


class ListLikesView(ListView):
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


class ListCommentView(ListView):
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


class ListCommentDeleteView(ListView):
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


class DeleteCommentView(View):
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


class DeletePostView(DeleteView):
    """
    a view to delete a post
    """
    model = Post
    success_url = reverse_lazy('show_profile')


class EditPostView(UpdateView):
    """
    a view to edit a post
    """
    model = Post
    fields = ['caption']
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy('show_profile')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class SearchView(View):
    """View to search username"""

    def post(self, request):
        input_search = request.POST.get('input_search', '').strip()
        profile = Profile.objects.filter(user_name__icontains=input_search)
        return render(request, 'posts/search_result.html', {'profile': profile})


class FollowRequestView(View):
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


class CancelNotificationView(View):
    def post(self, request, pk):
        receiver = get_object_or_404(User, pk=pk)
        Notification.objects.filter(
            to_user=receiver,
            from_user=request.user,
            notification_type='follow'
        ).delete()
        return redirect(reverse('show_profile_user', args=[pk]))




