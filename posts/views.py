from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View, DeleteView
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


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'posts/confirm_delete.html'
    success_url = '/posts/show_profile'


