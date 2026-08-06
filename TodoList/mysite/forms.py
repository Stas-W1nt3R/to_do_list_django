from django import forms
from .models import Blog, Comment, Profile


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "description", "tag"]
        widgets = {
            "tag": forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
