# Import the render function to generate an HttpResponse using a template
from django.shortcuts import render

# Define the homepage view
def homepage(request):
 return render(request, 'core/homepage.html')
