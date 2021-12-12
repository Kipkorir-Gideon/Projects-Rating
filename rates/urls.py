from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from . import views
from . import views as app_views

urlpatterns=[
    path('',views.projects,name='projects'),
    path('profile/<pk>', views.profile, name='profile'),
    re_path(r'^search/$',app_views.search_projects,name='search'),

]
if settings.DEBUG:

    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)