from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User, Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_name', 'profile_pic', 'bio']
