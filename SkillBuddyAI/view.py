from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from SkillBuddyAI.forms import SingUpForm


def home(request):
    # print("Home")
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(home)
    else:
        form = SingUpForm()
    return  render(request,'signup.html',{'form':form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully!')
            return redirect('/')  # Redirect to home or dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def TaskManager(request):
    return render(request, 'TaskManager.html')