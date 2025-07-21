from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, FormView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreateUserForm, EditProfileForm
from django.utils import timezone

from accounts.models import User, Profile
from posts.models import Post, Notification, Follow


# Create your views here.

class SignUpView(CreateView):
    """
    class SignUp for create new user
    """
    form_class = CreateUserForm
    template_name = "registration/signup.html"
    success_url = "/accounts/login/"


class EditeProfileView(UpdateView ,LoginRequiredMixin):
    """
    class edit profile login user
    """
    model = Profile
    form_class = EditProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = "/posts/index/"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        form.instance.is_complete = True
        form.instance.date_joined = timezone.now()
        return super().form_valid(form)


class ShowProfileView(TemplateView ,LoginRequiredMixin):
    """
    class show profile login user
    """
    template_name = "accounts/show_my_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        post = Post.objects.filter(user=self.request.user)
        context['post'] = post
        return context


class ShowProfileUserView(View, LoginRequiredMixin):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        user_sender = request.user
        user_receiver = profile.user


        follow_requested = Notification.objects.filter(
            notification_type='follow',
            from_user=user_sender,
            to_user=user_receiver
        ).exists()
        is_following = Follow.objects.filter(follower=request.user, following=profile.user).exists()

        is_owner = user_sender == user_receiver

        context = {
            'profile': profile,
            'follow_requested': follow_requested,
            'is_owner': is_owner,
            'is_following': is_following,
        }

        return render(request, 'accounts/show_user_profile.html', context)