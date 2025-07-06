from backend.tasks import do_import
from django.core.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        do_import.delay()