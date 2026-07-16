from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import UserForm, BlogForm, CommentForm


def MainPage(request):
    return render(request, 'MainPage.html')

def registration(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            userform.save()
            return redirect('MainPage')
        else:
            return HttpResponse("<h2>Данные некорректные!</h2>")
    else:
        userform = UserForm()
        return render(request,'registration.html',{"form":userform})