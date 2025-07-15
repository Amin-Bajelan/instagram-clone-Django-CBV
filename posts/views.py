from django.shortcuts import render
from django.views.generic import ListView,TemplateView
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