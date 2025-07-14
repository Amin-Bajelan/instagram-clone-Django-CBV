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
        return context