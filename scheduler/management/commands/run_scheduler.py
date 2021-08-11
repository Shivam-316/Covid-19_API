import logging
import pytz
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from ._private import init_data

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class Command(BaseCommand):
    help = 'Run blocking scheduler to create periodical tasks'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Started scheduler'))

        init_data()

        self.stdout.write(self.style.NOTICE('Finised scheduler'))
