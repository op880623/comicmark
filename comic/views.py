from django.shortcuts import render
from django.http import HttpResponse

from .models import Comic

def index(request):
    comics = Comic.objects.all()
    return render(request, 'comic/index.html', {'comics': comics})
