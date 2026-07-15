from django.http import HttpResponse
from django.shortcuts import render
from .forms import *


def index(request):
    if request.method =="POST":
        user = UserForm(request.POST)
        if user.is_valid():
            username = user.cleaned_data['username']
            password = user.cleaned_data['password']
            email = user.cleaned_data['email']
            return HttpResponse(f"<h2>Привет {username} c почтой: {email}</h2>")
        else:
            return HttpResponse("Invalid Data")
    else:
        user = UserForm()
        return render(request,'index.html',{'form':user})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def task(request, id):
    return HttpResponse(f"Задача {id}")