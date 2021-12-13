from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = CloudinaryField(blank=True, default = 'photo')

    #Creates a profile when a user is created
    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    #Saves the User's profile information
    @receiver(post_save, sender = User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_user_profile(self):
        self.save()

    def delete_user_profile(self):
        self.delete()

    def __str__(self):
        return "%s profile" % self.user



class Projects(models.Model):
    title = models.CharField(max_length=100)
    screenshot = CloudinaryField('image')
    description = models.TextField()
    day_posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    site_url = models.URLField()

    def save_user_project(self):
        self.save()

    def delete_user_project(self):
        self.delete()

    @classmethod
    def get_user_project(cls):
        projects = cls.objects.all()
        return projects

    @classmethod
    def search_user_project(cls, search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects

    @classmethod
    def get_project_by_owner(cls, owner):
        projects = cls.objects.filter(owner=owner)
        return projects

    @classmethod
    def get_project_by_id(cls, project_id):
        try:
            project = Projects.objects.get(project_id=project_id)

        except ObjectDoesNotExist:
            raise Http404()

        return project

    def __str__(self):
        return "%s projects" % self.title



class Rates(models.Model):
    design = models.IntegerField(default=0,blank=True,validators=[MinValueValidator(1),MaxValueValidator(10)])
    usability = models.IntegerField(default=0,blank=True,validators=[MinValueValidator(1),MaxValueValidator(10)])
    content = models.IntegerField(default=0,blank=True,validators=[MinValueValidator(1),MaxValueValidator(10)])
    design_average = models.FloatField(default=0.0,blank=True)
    usability_average = models.FloatField(default=0.0,blank=True)
    content_average = models.FloatField(default=0.0,blank=True)
    aggregate = models.FloatField(default=0.0,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects,on_delete=models.CASCADE)

    def save_rates(self):
      self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rates.objects.filter(project_id=id).all()
        return ratings

    def __str__(self):
        return "%s rates" % self.aggregate