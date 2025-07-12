from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
