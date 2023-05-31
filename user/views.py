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
            if user.is_staff:
                return redirect('teacher-dashboard')
            else:
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # Additional fields specific to the Faculty or Student model
        phone = request.POST['phone']
        profile_pic = request.FILES.get('profile_pic')

        # Create a new Faculty or Student instance based on the provided form data
        if request.POST.get('is_faculty'):
            user = Faculty(username=username, phone=phone)
        else:
            user = Student(username=username, phone=phone)

        if password == confirm_password:
            user.set_password(password)
            user.save()
            # Redirect to the desired page after successful signup
            return redirect('login')
        else:
            # Handle password mismatch
            return render(request, 'user/signup.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'user/signup.html')


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


