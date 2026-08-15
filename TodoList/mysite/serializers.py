from rest_framework import serializers
from .models import Blog, Comment, Tag
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "comment", "date"]


class BlogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tag = serializers.PrimaryKeyRelatedField(many=True, queryset = Tag.objects.all(), required=False)
    class Meta:
        model = Blog
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "description", "date", "tag", "user", "comment"]
