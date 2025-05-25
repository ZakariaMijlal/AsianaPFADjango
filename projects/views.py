from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import ProjectForm
from .forms import TaskForm
from .models import Task
from django.contrib.auth.models import User


def home(request):
    return render(request,'projects/home.html')

def custom_logout(request):
    logout(request)
    return redirect('logged_out')

def custom_logout(request):
    logout(request)
    return redirect('home')


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = Task.objects.filter(project=project, user=request.user)  # Filter tasks by project and user
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)  # Filter tasks by user
    return render(request, 'projects/project_list.html', {'projects': projects, 'tasks': tasks})

@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project-list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()  # Save the many-to-many data for the form
            return redirect('project-list')
    else:
        form = TaskForm()
    return render(request, 'projects/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project-detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'projects/task_edit.html', {'form': form})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project-detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_edit.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk  # Save project ID before deleting task
    task.delete()
    return HttpResponseRedirect(reverse('project-detail', args=[project_pk]))
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project-list')
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        project_pk = task.project.pk  # Save project ID before deleting task
        task.delete()
        return HttpResponseRedirect(reverse('project-detail', args=[project_pk]))
    return render(request, 'projects/task_confirm_delete.html', {'task': task})