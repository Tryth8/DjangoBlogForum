from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['topic', 'name', 'description']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']