"""
URL configuration for TodoList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from mysite import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from mysite.api import UserViewSet, BlogViewSet, TagViewSet, CommentViewSet
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"blogs", BlogViewSet)
router.register(r"tags", TagViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path("admin/", admin.site.urls),
    path("", views.MainPage_view, name="MainPage"),
    path("registration/", views.registration_view, name="registration"),
    path("enter/", views.enter_view, name="enter"),
    path("exit/", views.exit_view, name="exit"),
    path("create/", views.create_blog_view, name="create"),
    path("edit/<int:id>", views.update_blog_view, name="edit"),
    path("blog/<int:id>", views.blog_view, name="blog"),
    path("delete/<int:id>", views.delete_blog_view, name="delete"),
    path("profile/<int:id>", views.profile_view, name="profile"),
    path("profile_edit/<int:id>", views.profile_edit_view, name="profile_edit"),
    path("search/", views.blog_search, name="search"),
    path("tag/<slug:slug>", views.blog_tag_view, name="tag"),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
