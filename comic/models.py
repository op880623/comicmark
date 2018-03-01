from django.db import models
from django.db.models.deletion import PROTECT, CASCADE

class Comic(models.Model):
    comicId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    newest = models.ForeignKey('Episode', on_delete=PROTECT, related_name='newest')
    progress = models.ForeignKey('Episode', on_delete=PROTECT, related_name='progress')

class Episode(models.Model):
    index = models.IntegerField()
    url = models.CharField(max_length=200)
    comic = models.ForeignKey(Comic, on_delete=CASCADE)
