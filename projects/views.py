from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import search_projects, paginate_projects
from .models import Project
from .forms import ProjectForm
# Create your views here.


def projects(request):

    projects, search_query = search_projects(request)

    custom_range, projects = paginate_projects(request, projects, 3)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context = {
        'project': projectObj,
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, f'The project "{
                             project}" is created successfully!')
            return redirect('projects')
    context = {
        'form': form,
    }
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            projects = form.save(commit=False)
            projects.owner = profile
            projects.save()
            messages.success(request, f'The project "{
                             project}" is updated successfully!')
            return redirect('projects')
    context = {
        'form': form,
    }
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project_name = project.name
        project.delete()
        messages.success(request, f'The project "{
                         project_name}" has been deleted successfully!')
        return redirect('projects')
    return render(request, 'delete-template.html', {'obj': project})
