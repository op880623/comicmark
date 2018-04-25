from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch

from .models import Comic, Episode

def index(request):
    updated = []
    unupdated = []
    for comic in Comic.objects.order_by('-updateTime').prefetch_related(
        Prefetch('episode_set', queryset=Episode.objects.order_by('index')),
        Prefetch('progress', queryset=Episode.objects.only('index'))
    ):
        if comic.is_updated():
            updated.append(comic)
        else:
            unupdated.append(comic)
    return render(request, 'comic/index.html',
        {'updated': updated, 'unupdated': unupdated})

def update_progress(request, comicId):
    comic = Comic.objects.get(comicId = comicId)
    comic.progress_id = comic.next_id
    comic.next = comic.episode(comic.next.index + 1)
    if comic.episode_exists(comic.progress.index - 1):
        comic.episode(comic.progress.index - 1).delete()
    comic.save()
    return redirect('index')

def add_comic(request):
    try:
        comicId = int(request.POST.get('comicId'))
    except:
        return redirect('index')
    try:
        progress = int(request.POST.get('progress'))
    except:
        progress = None
    comic = Comic.new(comicId)
    comic.update(progress)
    return redirect('index')

def delete_comic(request, comicId):
    Comic.objects.get(comicId = comicId).delete()
    return redirect('index')
