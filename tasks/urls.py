from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:project_id>/create/',
         views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('<int:task_id>/close/', views.task_close, name='task_close'),
    path('tasks/<int:task_id>/toggle_complete/',
         views.task_toggle_complete, name='task_toggle_complete'),
]
