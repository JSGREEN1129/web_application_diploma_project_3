from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.hashers import check_password

from .models import Task
from .forms import TaskForm, TaskEditForm
from projects.models import Project


@login_required
@never_cache
def task_create(request, project_id):
    # Ensure only the project owner can add tasks
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Link task to the correct project
            task.save()
            task.check_status()  # Ensure status is up-to-date
            messages.success(
                request, f"Task '{task.name}' created successfully!")
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_create.html', {'form': form, 'project': project})


@login_required
@never_cache
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)

    task.check_status()  # Refresh status before showing

    error_task_id = request.GET.get('error_task_id', '')  # Used for modal error re-display

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'error_task_id': error_task_id,
    })


@login_required
@never_cache
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    project = task.project

    redirect_to = request.GET.get('next', reverse(
        'project_detail', kwargs={'project_id': project.id}))

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.check_status()  # Update status after changes
            task.save()
            messages.success(
                request, f"Task '{task.name}' updated successfully!")
            return redirect(redirect_to)
    else:
        form = TaskEditForm(instance=task)

    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task, 'project': project, 'next': redirect_to})


@login_required
@never_cache
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    project = task.project

    # Get redirect path from POST or fallback to project page
    next_url = request.POST.get('next') or reverse(
        'project_detail', kwargs={'project_id': project.id})

    if request.method == 'POST':
        password = request.POST.get('password', '')

        # Secure password check
        if not password or not check_password(password, request.user.password):
            if '?' in next_url:
                redirect_url = f"{next_url}&error_task_id={task.id}"
            else:
                redirect_url = f"{next_url}?error_task_id={task.id}"
            return redirect(redirect_url)

        task.delete()
        messages.success(request, f"Task '{task.name}' deleted successfully!")
        return redirect(next_url)

    return redirect(next_url)


@login_required
@never_cache
def task_close(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    task.status = 'completed'
    task.check_status()
    task.save()
    messages.success(request, f"Task '{task.name}' closed successfully!")
    return redirect('project_detail', project_id=task.project.id)


@login_required
@never_cache
def task_toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)

    if task.status == 'completed':
        # Revert to previous or default to 'outstanding'
        prev_status = task.previous_status if task.previous_status else 'outstanding'
        task.status = prev_status
        task.previous_status = None
        task.check_status()

        # Reopen project if needed
        project = task.project
        if project.status == 'closed':
            project.status = 'open'
            project.save()
            messages.info(
                request, f"Project '{project.name}' was reopened due to current tasks open and outstanding.")

        messages.success(request, f"Task '{task.name}' reopened.")

    else:
        # Mark as completed and store old status
        task.previous_status = task.status
        task.status = 'completed'
        task.check_status()
        messages.success(request, f"Task '{task.name}' marked as complete.")

    task.save()

    # Redirect to 'next' URL if present, else to project detail
    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)

    return redirect('project_detail', project_id=task.project.id)
