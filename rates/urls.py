from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from . import views
from . import views as app_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    path('',views.projects,name='projects'),
    path('profile/<pk>', views.profile, name='profile'),
    path('rating/<int:project_id>',app_views.rating,  name='rating'),
    path('api/projects/',app_views.ProjectList.as_view()),
    path('api/profiles/',app_views.ProfileList.as_view()),
    path('api_token/', obtain_auth_token),
    re_path(r'^search/$',app_views.search_projects,name='search'),

]
if settings.DEBUG:

    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)