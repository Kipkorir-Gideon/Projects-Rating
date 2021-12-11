from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'bio', 'user', 'photo')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'title', 'screenshot', 'description', 'day_posted', 'owner', 'url')