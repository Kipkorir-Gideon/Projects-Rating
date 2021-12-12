from django import forms
from django.contrib.auth.models import User
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'user', 'bio')



class ProjectForm(forms.ModelForm):
  class Meta:
    model = Projects
    fields = ['title', 'screenshot', 'description', 'owner', 'site_url']