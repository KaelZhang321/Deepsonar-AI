"""
User authentication views for the Django frontend.

Handles user registration, login, and logout functionality.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    """Landing page view."""
    return render(request, 'index.html')


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        # Redirect to Chainlit if already logged in
        return redirect('http://localhost:8001')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Redirect to Chainlit app
                return redirect('http://localhost:8001')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('http://localhost:8001')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            # Redirect to Chainlit app
            return redirect('http://localhost:8001')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
