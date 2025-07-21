from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # url api see list all posts with filter
    path('posts/', views.PostListAPIView.as_view(), name='index'),
    # url api see posts detail
    path('posts/<int:pk>/', views.PostDetailAPIView.as_view(), name='detail'),

    # url jwt token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]