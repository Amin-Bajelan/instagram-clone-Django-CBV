from django.urls import path,include
from . import views

urlpatterns = [
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('show_profile/', views.ShowProfileView.as_view(), name='show_profile'),
    path('edite_profile/',views.EditeProfileView.as_view(),name='edite_profile'),
]