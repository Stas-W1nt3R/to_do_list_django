from django import forms
from django.contrib.auth.models import User
from .models import User, Blog, Comment


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','description','date','user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','user','blog','date']