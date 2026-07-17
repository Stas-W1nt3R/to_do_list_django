from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import BlogForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login, logout


def MainPage(request):
    return render(request, 'MainPage.html')

def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MainPage')
        else:
            return HttpResponse("<h2>Данные некорректные!</h2>")
    else:
        form = UserCreationForm()
        return render(request,'registration.html',{"form":form})

def enter(request):
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
                return HttpResponse("<h2>Неверное имя пользователя или пароль!</h2>")
        else:
            return HttpResponse("<h2>Данные некорректные!</h2>")
    else:
        form = AuthenticationForm()
        return render(request,'enter.html',{"form":form})