from django.core.management.base import BaseCommand, CommandError
from comic.models import Comic

class Command(BaseCommand):
    help = "add comic"

    def add_arguments(self, parser):
        parser.add_argument('comicId', nargs = 1, type = int)
        parser.add_argument('index', nargs = '?', default = None, type = int)

    def handle(self, *args, **options):
        comic = Comic.new(options['comicId'][0])
        comic.update(options['index'])
