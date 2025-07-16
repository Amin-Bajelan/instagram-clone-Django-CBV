from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, UpdateView, TemplateView

from .forms import CreateUserForm, EditProfileForm
from django.utils import timezone

from accounts.models import User, Profile
from posts.models import Post


# Create your views here.

class SignUpView(CreateView):
    """
    class SignUp for create new user
    """
    form_class = CreateUserForm
    template_name = "registration/signup.html"
    success_url = "/accounts/login/"


class EditeProfileView(UpdateView):
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


class ShowProfileView(TemplateView):
    """
    class show profile login user
    """
    template_name = "accounts/show_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        post = Post.objects.filter(user=self.request.user)
        context['post'] = post
        return context
