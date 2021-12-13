from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
@login_required
def projects(request):
    if request.method == 'POST':
        current_user = request.user
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
    form = ProjectForm()
    projects = Projects.objects.all()
    return render(request, 'projects.html', {'projects': projects, 'form': form})


# search projects 
@login_required
def search_projects(request):
    if 'search_project' in request.GET and request.GET["search_project"]:
        search_term = request.GET.get("search_project")
        searched_projects = Projects.search_user_project(search_term)
        message = f"{search_term}"
        form = ProjectForm()

        return render(request, 'search.html', {"message":message,"projects": searched_projects,"form":form})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})


@login_required
def profile(request, pk):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
        return redirect("projects")
    user = User.objects.get(pk=pk)
    c_user = request.user
    form = ProjectForm()
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user': user, 'form': form, 'profile_form': profile_form, "c_user": c_user})