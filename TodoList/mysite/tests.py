from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from mysite.models import Blog, Tag, Comment


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.tag = Tag.objects.create(name="Python", slug="python")

    def test_blog_creation(self):
        blog = Blog.objects.create(
            user=self.user, title="Test Blog", description="Test Description"
        )
        blog.tag.add(self.tag)

        self.assertEqual(blog.title, "Test Blog")
        self.assertEqual(blog.user.username, "testuser")
        self.assertEqual(blog.tag.count(), 1)

    def test_profile_created_on_user_creation(self):
        self.assertTrue(hasattr(self.user, "user_profile"))
        self.assertIsNotNone(self.user.user_profile)

    def test_comment_creation(self):
        blog = Blog.objects.create(
            user=self.user, title="Blog with comment", description="Desc"
        )
        comment = Comment.objects.create(
            user=self.user, blog=blog, comment="Nice post!"
        )
        self.assertEqual(str(comment), "Комментарий от testuser")
        self.assertEqual(blog.blog_comments.count(), 1)


class BlogAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apitest", password="testpass123")
        self.user2 = User.objects.create_user(
            username="apitest2", password="testpass1234"
        )
        self.tag = Tag.objects.create(name="Django", slug="django")
        self.blog = Blog.objects.create(
            user=self.user, title="API Test Blog", description="API Desc"
        )
        self.blog.tag.add(self.tag)

    def test_create_user(self):
        response = self.client.post(
            "/registration/",
            data={
                "username": "testuser2",
                "password1": "MyStr0ng!Pass#2024",
                "password2": "MyStr0ng!Pass#2024",
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_blog_by_non_author(self):
        self.client.force_login(self.user2)
        url = reverse("delete", args=[self.blog.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("недостаточно прав", response.content.decode())
        self.assertTrue(Blog.objects.filter(id=self.blog.id).exists())

    def test_get_blog_list(self):
        response = self.client.get("/api/blogs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        # Если пагинация включена — данные в 'results', иначе это список
        if isinstance(data, dict):
            results = data.get("results", [])
        else:
            results = data

        titles = [item["title"] for item in results]
        self.assertIn("API Test Blog", titles)

    def test_create_blog_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/blogs/",
            {"title": "New Blog", "description": "New Desc", "tag": [self.tag.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)

    def test_create_blog_anonymous(self):
        response = self.client.post(
            "/api/blogs/", {"title": "Hack Blog", "description": "Hack"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
