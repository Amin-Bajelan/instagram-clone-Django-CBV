from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.

class IndexView(ListView):
    models = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'