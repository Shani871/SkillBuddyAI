from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

from SkillBuddyAI.forms import SingUpForm

# Home view (protected for logged-in users)

def home(request):
    return render(request, 'index.html')

# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('login')  # Redirect to the profile page
    else:
        form = SingUpForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to profile if the user is already logged in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully!')
            return redirect('home')  # Redirect to the profile page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


# Profile view (protected for logged-in users)

def profile(request):
    return render(request, 'profile.html', {'user': request.user})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully!')
        return redirect('login')  # Redirect to the login page after logout
    return render(request, 'logout.html')
# Task Manager view (not protected)
def TaskManager(request):
    return render(request, 'TaskManager.html')