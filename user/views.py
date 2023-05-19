from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


# @login_required
# def home(request):
#     context = {

#     }

#     return render(request, 'user/profile.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('lobby')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'user/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


def signup(request):

    form = UserRegisterForm()

    context = {
        "pageTitle": "SpectaX-Sign Up",
        "form": form,
    }
    return render(request, "user/signup.html", context)


def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_staff:
        info = user.faculty
    else:
        info = user.student

    print("Profile detail:")
    print(info)

    context = {
        'user': user,
        'info': info,
    }
    return render(request, 'user/profile.html', context)
