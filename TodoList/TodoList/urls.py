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
from django.urls import path
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.MainPage_view, name='MainPage'),
    path('registration/', views.registration_view, name='registration'),
    path('enter/', views.enter_view, name='enter'),
    path('exit/', views.exit_view, name='exit'),
    path('create/', views.create_blog_view, name='create'),
    path('edit/<int:id>', views.update_blog_view, name='edit'),
    path('blog/<int:id>', views.blog_view, name='blog'),
    path('delete/<int:id>', views.delete_blog_view, name='delete'),
]
