from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index_post'),
    path('explore/', views.ExploreView.as_view(), name='explore_post'),
]