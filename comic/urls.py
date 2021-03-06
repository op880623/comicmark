from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(
        r'^comic/(?P<comicId>\d+)/update_progress$',
        views.update_progress,
        name = 'update_progress'
    ),
    re_path(
        r'^comic$',
        views.add_comic,
        name = 'add_comic'
    ),
    re_path(
        r'^comic/(?P<comicId>\d+)$',
        views.delete_comic,
        name = 'delete_comic'
    )
]
