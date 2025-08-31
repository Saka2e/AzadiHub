from django.core.management.base import BaseCommand
from crawler.tasks import main

class Command(BaseCommand):
    help = 'Update configs from crawler'

    def handle(self, *args, **options):
        main()
        self.stdout.write(self.style.SUCCESS('Configs updated successfully!'))