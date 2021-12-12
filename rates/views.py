from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
def projects(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
    form = ProjectForm()
    projects = Projects.objects.all()
    return render(request, 'projects.html', {'projects': projects, 'form': form})


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