from django.shortcuts import render
from .models import *

# Create your views here.
def projects(request):
    projects = Projects.objects.all()
    return render(request, 'projects.html', {'projects': projects})
    