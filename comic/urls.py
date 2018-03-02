from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^comic/(?P<comicId>\d+)/update_progress$', views.update_progress)
]
