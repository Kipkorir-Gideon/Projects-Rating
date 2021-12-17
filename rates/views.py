from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import Http404,HttpResponseRedirect
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
# @login_required
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
        form = ProjectForm()
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message,"form":form})


@login_required
def profile(request, pk):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
        return redirect("projects")
    user = User.objects.get(pk=pk)
    c_user = request.user
    projects = Projects.objects.filter(id = c_user.id).all()
    form = ProjectForm()
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user': user, 'Projects': projects, 'form': form, 'profile_form': profile_form, "c_user": c_user})


@login_required
def rating(request, project_id):
    c_user = request.user
    rates = Rates.objects.filter(project_id=project_id).all()
    project = Projects.objects.get(pk=project_id)
    ratings = Rates.objects.filter(project=project_id,user=request.user).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        rating_form = RatingsForm(request.POST)
        if rating_form.is_valid():
            rate = rating_form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            project_ratings = Rates.objects.filter(project=project_id)

            design = [design.design for design in project_ratings]
            design_average = sum(design) / len(design)
            usability = [usability.usability for usability in project_ratings]
            usability_average = sum(usability) / len(usability)
            content = [content.content for content in project_ratings]
            content_average = sum(content) / len(content)

            aggregate = (design_average + usability_average + content_average)/3
            print(aggregate)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.aggregate = round(aggregate, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = ProjectForm()
        rating_form = RatingsForm()
    return render(request, 'rating.html', {'rating_form': rating_form,'form': form,'c_user': c_user,'rates': rates,'project': project,'rating_status':rating_status})



class ProjectList(APIView):
  def get(self,request,format=None):
    all_projects=Projects.objects.all()
    serializers=ProjectSerializer(all_projects,many=True)
    return Response(serializers.data)

class ProfileList(APIView):
  def get(self,request,format=None):
    all_profiles=Profile.objects.all()
    serializers=ProfileSerializer(all_profiles,many=True)
    return Response(serializers.data)