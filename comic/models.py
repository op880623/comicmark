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
    updateTime = models.DateTimeField()
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
    next = models.ForeignKey(
        'Episode',
        blank = True,
        null = True,
        on_delete = SET_NULL,
        related_name = 'next'
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
        comic.updateTime = timezone.now()
        comic.save()
        return comic

    def update(self, progress = None):
        # determine progress number
        if not isinstance(progress, int):
            progress = self.progress and self.progress.index or -100

        for ep in self.episodes().iterator():
            if ep.index < progress:
                ep.delete()

        # get page
        page = requests.get(self.url)
        page.encoding = 'big5'

        # build episodes
        pattern = 'href=(/comic/%s(\d{4})(\d)\d{6}.html)' % str(self.comicId)
        for a_tag in re.finditer(pattern, page.text):
            index = int(a_tag.group(2))
            if index >= progress and not self.episode_exists(index):
                url = "http://www.cartoonmad.com" + a_tag.group(1)
                unit = a_tag.group(3) == '2' and '話' or '卷'
                e = self.episode_set.create(
                    index = index,
                    url = url,
                    unit = unit
                )
                self.updateTime = timezone.now()

        # find progress and next episode
        self.progress = self.episode(progress)
        if self.progress:
            self.next = self.episode(progress + 1)
        else:
            self.next = self.episodes().first()

        # find newest episode
        self.newest = self.episodes().only('comic_id').last()

        # save and return
        self.save()
        return None

    def episode_exists(self, index):
        return self.episode_set.filter(index = index).only('id').exists()

    def episode(self, index):
        episodes = self.episode_set.filter(index = index)
        if bool(episodes):
            return episodes[0]
        else:
            return None

    def episodes(self):
        return self.episode_set.order_by('index')

    def is_updated(self):
        return self.newest_id != self.progress_id

    @classmethod
    def json_to_progress(cls, records):
        records = json.loads(records)
        for record in records:
            c = Comic.new(record['comicId'])
            c.update(record['index'])


class Episode(models.Model):
    index = models.IntegerField()
    url = models.CharField(max_length = 200)
    unit = models.CharField(max_length = 10, default = '話')
    comic = models.ForeignKey(Comic, on_delete = CASCADE)

    def __str__(self):
        return '%s 第 %s %s' % (self.comic.name, self.index, self.unit)

    def is_progress(self):
        return self.id == self.comic.progress_id

    def is_next(self):
        return self.id == self.comic.next_id
