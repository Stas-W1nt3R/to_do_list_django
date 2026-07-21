from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from .forms import BlogForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .models import Blog


def MainPage_view(request):
    blogs = Blog.objects.all()

    return render(request, 'MainPage.html', {'blogs':blogs})

def registration_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MainPage')
        else:
            return HttpResponse(form.errors)
    else:
        form = UserCreationForm()
        return render(request,'registration.html',{"form":form})

def enter_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('MainPage')
            else:
                return HttpResponse(form.errors)
        else:
            return HttpResponse(form.errors)
    else:
        form = AuthenticationForm()
        return render(request,'enter.html',{"form":form})

def exit_view(request):
    logout(request)
    return redirect('MainPage')

def create_blog_view(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            redirect('enter')

        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('MainPage')
        else:
            return HttpResponse(form.errors)
    else:
        form = BlogForm()
        return render(request,'create_blog.html',{"form":form})

def blog_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if not request.user.is_authenticated:
            return redirect('enter')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect('blog', id=blog.id)
        else:
            return HttpResponse(form.errors)

    else:
        form = CommentForm()
        return render(request,'blog_page.html',{'blog':blog,'form':form})

def update_blog_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.user != request.user:
        return HttpResponse("У вас нет прав на редактирование этого поста!!!")

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)

        if form.is_valid():
            form.save()
            return redirect('blog', id=id)

        else:
            return HttpResponse(form.errors)


    else:
        form = BlogForm(instance=blog)
        return render(request,'create_blog.html',{"form":form})

def delete_blog_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.user != request.user:
        return HttpResponse("У вас недостаточно прав для удаления этого поста!!!")

    if request.method == "POST":
        blog.delete()
        return redirect('MainPage')
    else:
        return render(request,'delete_blog.html',{"blog":blog})