from .models import Blog, Comment, Tag
from django.contrib.auth.models import User
from .serializers import (
    BlogSerializer,
    CommentSerializer,
    TagSerializer,
    UserSerializer,
)
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorOrReadOnly


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by("date")
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Blog.objects.all()
        tag = self.request.query_params.get("tag")
        if tag:
            queryset = queryset.filter(tag__slug=tag)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], description="Возвращает 3 последних блога")
    def latest(self, request):
        blogs = Blog.objects.all().order_by("-date")[:3]
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated], description="Возвращает все блоги пользователя")
    def my_blogs(self,request):
        blogs = Blog.objects.filter(user=self.request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=True,methods=["get", "post"], permission_classes=[IsAuthenticatedOrReadOnly], description="Комментарии к блогу")
    def comments(self,request,pk=None):
        blog = self.get_object()

        if request.method == "GET":
            comments = Comment.objects.filter(blog=blog)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("date")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
