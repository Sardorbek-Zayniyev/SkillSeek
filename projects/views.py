from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import search_projects, paginate_projects, clean_tags
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm

# Create your views here.


def projects(request):

    projects, search_query = search_projects(request)

    custom_range, projects = paginate_projects(request, projects, 6)

    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            projectObj.get_vote_count
            messages.success(request, "Your review was seccessfully submitted !")
            return redirect("project", pk=projectObj.id)
    else:
        form = ReviewForm()
    context = {
        "project": projectObj,
        "form": form,
    }
    return render(request, "projects/single-project.html", context)


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        new_tags = clean_tags(request.POST.get("new_tags", ""))
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in new_tags:
                tag, create = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            project.save()
            messages.success(
                request,
                f'The project "{
                             project}" is created successfully!',
            )
            return redirect("projects")
    context = {
        "form": form,
    }
    return render(request, "projects/project-form.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        new_tags = clean_tags(request.POST.get("new_tags", ""))
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            for tag in new_tags:
                tag, create = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            project.save()
            messages.success(
                request,
                f'The project "{
                             project}" is updated successfully!',
            )
            return redirect("update_project", pk=project.id)
    context = {
        "form": form,
        "project": project,
    }
    return render(request, "projects/project-form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project_name = project.name
        project.delete()
        messages.success(
            request,
            f'The project "{
                         project_name}" has been deleted successfully!',
        )
        return redirect("projects")
    return render(request, "delete-template.html", {"obj": project})
