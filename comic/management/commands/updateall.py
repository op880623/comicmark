from django.core.management.base import BaseCommand, CommandError
from comic.models import Comic

class Command(BaseCommand):
    help = "Update all comics"

    def handle(self, *args, **options):
        for comic in Comic.objects.iterator():
            comic.update()
