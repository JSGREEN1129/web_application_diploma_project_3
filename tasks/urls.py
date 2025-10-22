from django.urls import path
from . import views

urlpatterns = [
    # Create a new task under a specific project
    path('project/<int:project_id>/create/',
         views.task_create, name='task_create'),

    # View the detail of a specific task
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),

    # Edit a specific task
    path('<int:task_id>/edit/', views.task_edit, name='task_edit'),

    # Delete a specific task
    path('<int:task_id>/delete/', views.task_delete, name='task_delete'),

    # Close a task (could be legacy or unused if toggle_complete replaces it)
    path('<int:task_id>/close/', views.task_close, name='task_close'),

    # Toggle the task's completion status (complete ↔ reopen)
    path('tasks/<int:task_id>/toggle_complete/',
         views.task_toggle_complete, name='task_toggle_complete'),
]
