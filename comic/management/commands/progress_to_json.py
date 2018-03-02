import json

from django.core.management.base import BaseCommand, CommandError
from comic.models import Comic

class Command(BaseCommand):
    help = "print comicId and progress index as json string"

    def handle(self, *args, **options):
        records = []
        for comic in Comic.objects.all():
            records.append({
                "comicId": comic.comicId,
                "index": comic.progress.index
            })
        print(json.dumps(records))
