from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm, CommentForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Blog, Comment, Tag, Profile


def MainPage_view(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "MainPage.html", {"page_obj": page_obj})


def registration_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("MainPage")
        else:
            return HttpResponse(form.errors)
    else:
        form = UserCreationForm()
        return render(request, "registration.html", {"form": form})


def enter_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("MainPage")
            else:
                return HttpResponse(form.errors)
        else:
            return HttpResponse(form.errors)
    else:
        form = AuthenticationForm()
        return render(request, "enter.html", {"form": form})


def exit_view(request):
    logout(request)
    return redirect("MainPage")


def create_blog_view(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            redirect("enter")

        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect("MainPage")
        else:
            return HttpResponse(form.errors)
    else:
        form = BlogForm()
        return render(request, "create_blog.html", {"form": form})


def blog_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if not request.user.is_authenticated:
            return redirect("enter")

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect("blog", id=blog.id)
        else:
            return HttpResponse(form.errors)

    else:
        form = CommentForm()
        return render(request, "blog_page.html", {"blog": blog, "form": form})


def update_blog_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.user != request.user:
        return HttpResponse("У вас нет прав на редактирование этого поста!!!")

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)

        if form.is_valid():
            form.save()
            return redirect("blog", id=id)

        else:
            return HttpResponse(form.errors)

    else:
        form = BlogForm(instance=blog)
        return render(request, "create_blog.html", {"form": form})


def delete_blog_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.user != request.user:
        return HttpResponse("У вас недостаточно прав для удаления этого поста!!!")

    if request.method == "POST":
        blog.delete()
        return redirect("MainPage")
    else:
        return render(request, "delete_blog.html", {"blog": blog})


def profile_view(request, id):
    if request.user.is_authenticated:
        profile_user = get_object_or_404(User, id=id)
        return render(request, "profile.html", {"profile_user": profile_user})
    else:
        return redirect("enter")


def profile_edit_view(request, id):
    if request.user.is_authenticated:
        if request.user.id == id:
            user = get_object_or_404(User, id=id)
            profile = Profile.objects.get(user=user)

            if request.method == "POST":
                form = ProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    return redirect("profile", id=id)
                else:
                    return HttpResponse(form.errors)

            else:
                form = ProfileForm(instance=profile)
                return render(request, "profile_edit.html", {"form": form})
        else:
            return HttpResponse(
                "У вас недостаточно прав для редактирования этой страницы!"
            )
    else:
        return redirect("enter")


def blog_search(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Blog.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, "blog_list.html", {"results": results})


def blog_tag_view(request, slug):
    if request.user.is_authenticated:
        tag = get_object_or_404(Tag, slug=slug)
        return render(request, "tag_view.html", {"tag": tag})
    else:
        return redirect("enter")
