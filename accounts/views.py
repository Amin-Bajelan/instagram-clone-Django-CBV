from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import CreateUserForm

# Create your views here.

class SignUpView(CreateView):
    """
    class SignUp for create new user
    """
    form_class = CreateUserForm
    template_name = "registration/signup.html"
    success_url = "/accounts/login/"
