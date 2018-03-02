import re
import requests
import json

from django.db import models
from django.utils import timezone
from django.db.models.deletion import SET_NULL, CASCADE

class Comic(models.Model):
    comicId = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    url = models.CharField(max_length = 200)
    updateTime = models.DateTimeField(default = timezone.now())
    newest = models.ForeignKey(
        'Episode',
        blank = True,
        null = True,
        on_delete = SET_NULL,
        related_name = 'newest'
    )
    progress = models.ForeignKey(
        'Episode',
        blank = True,
        null = True,
        on_delete = SET_NULL,
        related_name = 'progress'
    )

    def __str__(self):
        return self.name

    @classmethod
    def new(cls, comicId):
        # create or get model
        if Comic.objects.filter(comicId = comicId).exists():
            return Comic.objects.get(comicId = comicId)
        else:
            comic = cls(comicId = comicId)

        # find url
        domain = "http://www.cartoonmad.com"
        comicId = str(comic.comicId)
        comic.url = "%s/comic/%s.html" % (domain, comicId)

        # find name
        page = requests.get(comic.url)
        page.encoding = 'big5'
        pattern = '<a href=/comic/%s.html>(.+)</a>' % comicId
        comic.name = re.search(pattern, page.text).group(1)

        # save and return
        comic.save()
        return comic

    def update(self, progress = None):
        # determine progress number
        try:
            if progress is None:
                progress = self.progress.index
        except:
            progress = 0

        for ep in self.episodes():
            if ep.index < progress:
                ep.delete()

        # get page
        page = requests.get(self.url)
        page.encoding = 'big5'

        # build episodes
        pattern = 'href=(/comic/%s(\d{4})\d{7}.html)' % str(self.comicId)
        for a_tag in re.findall(pattern, page.text):
            index = int(a_tag[1])
            if index >= progress:
                if not Episode.objects.filter(index = index, comic = self).exists():
                    url = "http://www.cartoonmad.com" + a_tag[0]
                    e = Episode(index = index, url = url, comic = self)
                    e.save()
                    self.updateTime = timezone.now()

        # find progress episode
        self.progress = Episode.objects.filter(index = progress, comic = self).get()

        # find newest episode
        newest = 0
        for ep in Episode.objects.filter(comic = self):
            if ep.index > newest:
                newest = ep.index
        self.newest = Episode.objects.filter(index = newest, comic = self).get()

        # save and return
        self.save()
        return None

    def episodes(self):
        return Episode.objects.filter(comic = self)

    @classmethod
    def json_to_progress(cls, records):
        for record in records:
            c = Comic.new(record['comicId'])
            c.update(record['index'])


class Episode(models.Model):
    index = models.IntegerField()
    url = models.CharField(max_length = 200)
    comic = models.ForeignKey(Comic, on_delete = CASCADE)

    def __str__(self):
        return '%s 第 %s 話' % (self.comic.name, self.index)

    def is_progress(self):
        if self == self.comic.progress:
            return True

    def is_next(self):
        if self.index == self.comic.progress.index + 1:
            return True
