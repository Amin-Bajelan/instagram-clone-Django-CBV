from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View
from .models import Post
from accounts.models import Profile


# Create your views here.

class IndexView(TemplateView):
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['posts'] = Post.objects.all()

        return context


class ExploreView(ListView):
    model = Post
    template_name = 'posts/explore.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user__profile__is_private=False).order_by('-date_posted')


class LikePostView(View):
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
    template_name = 'posts/likes_list.html'
    context_object_name = 'liked_users'
    model = Post

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        return post.liked_by.all()
