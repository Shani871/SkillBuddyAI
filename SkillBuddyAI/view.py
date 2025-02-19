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
def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to profile if already logged in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully!')
            next_url = request.GET.get('next', 'home')  # Redirect to the page user wanted
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in after signup
            next_url = request.GET.get('next', 'home')  # Redirect to the original page user wanted
            return redirect(next_url)
    else:
        form = SingUpForm()
    return render(request, 'signup.html', {'form': form})


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

def blog(request):
    return render(request, 'blog.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def portfolio (request):
    return render(request,'portfolio-details.html')


