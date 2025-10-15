from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode
from .models import Project
from .forms import ProjectForm

@login_required
@never_cache
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            messages.success(
                request, f'Project "{new_project.name}" was created successfully!'
            )
            return redirect("project_list")
    else:
        form = ProjectForm()

    return render(request, "projects/project_create.html", {"form": form})

@login_required
@never_cache
def project_list(request):
    status_filter = request.GET.get("status", "all")
    error_project_id = request.GET.get("error_project_id")
    error_message = request.GET.get("error_message")

    projects = Project.objects.filter(owner=request.user).prefetch_related("tasks")
    if status_filter in ["open", "closed"]:
        projects = projects.filter(status=status_filter)

    for project in projects:
        project.update_task_counts()

    context = {
        "projects": projects,
        "status_filter": status_filter,
        "error_project_id": error_project_id,
        "error_message": error_message,
    }
    return render(request, "projects/project_list.html", context)

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    status_filter = request.GET.get('status', 'all')
    error_task_id = request.GET.get('error_task_id')

    project.update_task_counts()

    if status_filter == 'completed':
        tasks = project.tasks.filter(status='completed')
    elif status_filter == 'outstanding':
        tasks = project.tasks.filter(status='outstanding')
    elif status_filter == 'overdue':
        tasks = project.tasks.filter(status='overdue')
    else:
        tasks = project.tasks.all().order_by('start_date')

    for task in tasks:
        task.check_status()

    completed_count = tasks.filter(status='completed').count()
    outstanding_count = tasks.filter(status='outstanding').count()
    overdue_count = tasks.filter(status='overdue').count()

    context = {
        'project': project,
        'tasks': tasks,
        'status_filter': status_filter,
        'completed_count': completed_count,
        'outstanding_count': outstanding_count,
        'overdue_count': overdue_count,
        'error_task_id': error_task_id,
    }
    return render(request, 'projects/project_detail.html', context)