from django.urls import path,include
from . import views

urlpatterns = [
    # url to sign up your account
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    # url contain all function (login, logout, change password, ...)
    path('accounts/', include('django.contrib.auth.urls')),
    # url to show login user profile
    path('show_profile/', views.ShowProfileView.as_view(), name='show_profile'),
    # url to edit login user profile
    path('edite_profile/',views.EditeProfileView.as_view(),name='edite_profile'),
    # url show searched profile user
    path('show_profile/<int:pk>/',views.ShowProfileUserView.as_view(),name='show_profile_user'),
]