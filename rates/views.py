from django.shortcuts import render
from .models import *

# Create your views here.
def projects(request):
    projects = Projects.objects.all()
    return render(request, 'projects.html', {'projects': projects})



# search projects 
def search_projects(request):
    if 'search_project' in request.GET and request.GET["search_project"]:
        search_term = request.GET.get("keyword")
        searched_projects = Projects.search_user_project(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})