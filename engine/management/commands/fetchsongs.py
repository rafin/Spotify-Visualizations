from django.core.management.base import BaseCommand
from spot.pl import store_db

class Command(BaseCommand):
    help = "Stores songs and playlist specified by first argument into database"

    def add_arguments(self, parser):
        parser.add_argument('playlist',nargs='+', type=str)

    def handle(self, *args, **options):
        playlist = ' '.join(options['playlist'])
        store_db(playlist)
