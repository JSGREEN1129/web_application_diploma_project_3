from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.project_create, name='project_create'),
    path('', views.project_list, name='project_list')
]