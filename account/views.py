from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserRegistrationForm, CustomUserLoginForm


# Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


# Login View
def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserLoginForm()
    return render(request, 'account/login.html', {'form': form})


# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
