from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts.models import Post


class PostListAPIView(ListCreateAPIView):
    """
    class posts(ListCreateAPIView):
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user', 'likes', 'num_comments', 'date_posted']
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    class posts detail (RetrieveUpdateDestroyAPIView):
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user', 'likes', 'num_comments', 'date_posted']
    queryset = Post.objects.all()
    serializer_class = PostSerializer
