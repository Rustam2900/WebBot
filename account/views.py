from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from account.forms import CustomUserRegistrationForm, CustomUserLoginForm, UserUpdateForm, ProfileUpdateForm
from account.models import VIPPackage
from django.contrib.auth.decorators import login_required


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


def home(request):
    return render(request, 'account/home.html')


def vip_package(request):
    packages = VIPPackage.objects.all()
    return render(request, 'account/vip_package.html', {'packages': packages})


@login_required
def my_account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account/my_account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'account/my_account.html', context)
