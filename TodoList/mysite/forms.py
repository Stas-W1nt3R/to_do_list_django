from django import forms
from django.contrib.auth.models import User
from .models import Blog, Comment
from django.contrib.auth.forms import UserCreationForm

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','description','date','user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','user','blog','date']