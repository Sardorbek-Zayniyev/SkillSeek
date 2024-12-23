from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .utils import search_profiles, paginate_profiles
from .models import Profile, User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm


def login_user(request):

    page = "login"

    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
            return render(request, "users/login-register.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(request.GET["next"] if "next" in request.GET else "account")
        else:
            messages.error(request, "Username or password is incorrect.")

    context = {"page": page}
    return render(request, "users/login-register.html", context)


def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


def register_user(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(
                request, f" {user.username} your account has been created successfully!"
            )
            login(request, user)
            return redirect("edit_account")
        else:
            messages.error(request, "???????????????????ERROR")
    context = {"form": form}
    return render(request, "users/login-register.html", context)


def profiles(request):

    profiles, search_query = search_profiles(request)

    custom_range, profiles = paginate_profiles(request, profiles, 6)

    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
        top_skills = profile.skill_set.exclude(description__exact="")
        other_skills = profile.skill_set.filter(description="")
        context = {
            "profile": profile,
            "top_skills": top_skills,
            "other_skills": other_skills,
        }
        return render(request, "users/user-profile.html", context)
    except Profile.DoesNotExist:
        messages.error(request, "The requested profile does not exist.")
        return redirect("profiles")


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
    }
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")
        messages.success(
            request,
            f'The profile "{
                         profile}" is updated successfully!',
        )

    context = {"form": form}
    return render(request, "users/profile-form.html", context)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(
                request,
                f'The skill "{
                             skill}" is created successfully!',
            )
            return redirect("account")
    else:
        form = SkillForm()
    context = {"form": form}
    return render(request, "users/skill-form.html", context)


@login_required(login_url="login")
def edit_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'The skill "{
                             skill}" is updated successfully!',
            )
            return redirect("account")
    else:
        form = SkillForm(instance=skill)
    context = {"form": form}
    return render(request, "users/skill-form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill_name = skill.name
        skill.delete()
        messages.success(
            request,
            f'The skill "{
                         skill_name}" has been deleted successfully!',
        )
        return redirect("account")
    return render(request, "delete-template.html", {"obj": skill})


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messages_user = profile.messages.all()
    for message in messages_user:
        print(message.name)
    unread_count = messages_user.filter(is_read=False).count()
    context = {
        "messages_user": messages_user,
        "unread_count": unread_count,
    }
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(
                request, f"Your message was successfully sent to {recipient}"
            )
            return redirect("user_profile", pk=recipient.id)
    else:
        form = MessageForm()
    context = {
        "recipient": recipient,
        "form": form,
    }
    return render(request, "users/message-form.html", context)
