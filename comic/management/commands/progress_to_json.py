import json

from django.core.management.base import BaseCommand, CommandError
from comic.models import Comic

class Command(BaseCommand):
    help = "print comicId and progress index as json string"

    def handle(self, *args, **options):
        records = [{
            "comicId": comic.comicId,
            "index": comic.progress and comic.progress.index or None
        } for comic in Comic.objects.order_by('updateTime').iterator()]
        print(json.dumps(records))
