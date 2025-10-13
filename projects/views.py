from django.shortcuts import render

# Create your views here.
def project_list(request):
    return render(request, "projects/project_list.html", context)

def project_create(request):
    return render(request, "projects/project_create.html", {"form": form})

def project_detail(request, project_id):
    return render(request, 'projects/project_detail.html', context)