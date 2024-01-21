from django import forms
from .models import Comment
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Photo

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'link']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# NEW CHANGES COMMENTS SECTION!!
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['url']