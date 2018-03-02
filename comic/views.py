from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Comic, Episode

def index(request):
    comics = Comic.objects.all()
    return render(request, 'comic/index.html', {'comics': comics})

def update_progress(request, comicId):
    comic = Comic.objects.get(comicId = comicId)
    comic.progress = Episode.objects.get(
        comic = comic,
        index = comic.progress.index + 1
    )
    comic.save()
    Episode.objects.get(
        comic = comic,
        index = comic.progress.index - 1
    ).delete()
    return redirect('index')
