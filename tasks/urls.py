from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:project_id>/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/edit/', views.task_edit, name='task_edit'),
]