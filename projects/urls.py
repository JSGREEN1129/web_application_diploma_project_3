from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.project_create, name='project_create'),
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('<int:project_id>/delete/', views.project_confirm_delete,
         name='project_confirm_delete'),
    path('<int:project_id>/toggle_complete/',
         views.project_toggle_complete, name='project_toggle_complete'),
]
