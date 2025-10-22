from django.urls import path
from . import views

# Define the URL patterns for the 'projects' app
urlpatterns = [
    # URL for creating a new project (e.g., /projects/create/)
    path('create/', views.project_create, name='project_create'),

    # URL for listing all projects (e.g., /projects/)
    path('', views.project_list, name='project_list'),

    # URL for viewing details of a single project by its ID (e.g., /projects/5/)
    path('<int:project_id>/', views.project_detail, name='project_detail'),

    # URL for editing a project (e.g., /projects/5/edit/)
    path('<int:project_id>/edit/', views.project_edit, name='project_edit'),

    # URL for confirming and handling project deletion (e.g., /projects/5/delete/)
    path('<int:project_id>/delete/', views.project_confirm_delete,
         name='project_confirm_delete'),

    # URL to toggle a project's completion status (mark as complete or reopen)
    path('<int:project_id>/toggle_complete/',
         views.project_toggle_complete, name='project_toggle_complete'),
]
