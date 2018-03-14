from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Comic, Episode

def index(request):
    comics = Comic.objects.all().order_by('-updateTime')
    return render(request, 'comic/index.html', {'comics': comics})

def update_progress(request, comicId):
    comic = Comic.objects.get(comicId = comicId)
    if comic.progress:
        comic.progress = comic.episode(comic.progress.index + 1)
        comic.episode(comic.progress.index - 1).delete()
    else:
        comic.progress = comic.episodes().first()
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
    comic = Comic.objects.get(comicId = comicId)
    comic.delete()
    return redirect('index')
