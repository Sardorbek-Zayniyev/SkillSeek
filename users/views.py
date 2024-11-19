from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, User



def login_user(request):

    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return render(request, 'users/login-register.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect.')

    context = {}
    return render(request, 'users/login-register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


@login_required(login_url='login')
def user_profile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
        top_skills = profile.skill_set.exclude(description__exact="")
        other_skills = profile.skill_set.filter(description="")
        context = {
            'profile': profile,
            'top_skills': top_skills,
            'other_skills': other_skills,
        }
        return render(request, 'users/user-profile.html', context)
    except Profile.DoesNotExist:
        messages.error(request, "The requested profile does not exist.")
        return redirect('profiles')
