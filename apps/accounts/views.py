from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import UserEditForm, RegisterForm
from django.urls import reverse
# from apps.accounts.forms import UserEditForm, SignupForm
from apps.accounts.models import User
#from django.contrib.auth.forms import AuthenticationForm

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Great job! You are registered!')
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }       
    return render(request, 'register.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, "Even better!  You are now logged out!")
    return redirect('home')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

