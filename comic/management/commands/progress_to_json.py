import json

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F

from comic.models import Comic

class Command(BaseCommand):
    help = "print comicId and progress index as json string"

    def handle(self, *args, **options):
        records = list(Comic.objects.values('comicId').annotate(
            index=F('progress__index')).order_by('updateTime'))
        print(json.dumps(records))
