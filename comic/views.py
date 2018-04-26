from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch, F

from .models import Comic, Episode

def index(request):
    comics = Comic.objects.order_by('-updateTime').prefetch_related(
        Prefetch('episode_set', queryset=Episode.objects.order_by('index'))
    )
    updated = list(comics.exclude(newest_id=F('progress_id')))
    unupdated = list(comics.filter(newest_id=F('progress_id')))
    return render(request, 'comic/index.html',
        {'updated': updated, 'unupdated': unupdated})

def update_progress(request, comicId):
    comic = Comic.objects.get(comicId = comicId)
    comic.progress = comic.next
    comic.next = comic.episode(comic.next.index + 1)
    comic.episode_set.filter(index = comic.progress.index - 1).delete()
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
