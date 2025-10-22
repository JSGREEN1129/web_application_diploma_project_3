# Import Django's path function to define URL routes
from django.urls import path

# Import views from the current app (core/views.py)
from . import views

# Define the list of URL patterns for this app
urlpatterns = [
    path('', views.homepage, name='homepage'),
]
