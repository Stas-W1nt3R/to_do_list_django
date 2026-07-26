from django import forms
from django.contrib.auth.models import User
from .models import Blog, Comment, Profile
from django.contrib.auth.forms import UserCreationForm

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','description','tag']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','bio']