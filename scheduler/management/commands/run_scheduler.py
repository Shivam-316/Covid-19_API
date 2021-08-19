from django.core.management.base import BaseCommand
from ._v1private import init_data

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Started scheduler'))

        init_data()

        self.stdout.write(self.style.NOTICE('Finised scheduler'))
