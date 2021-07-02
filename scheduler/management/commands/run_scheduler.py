import logging
import pytz
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from ._private import init_data

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class Command(BaseCommand):
    help = 'Run blocking scheduler to create periodical tasks'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Preparing scheduler'))

        scheduler = BlockingScheduler(timezone = pytz.timezone('Asia/Kolkata'))
        every_day_at_time = CronTrigger(hour=12, minute=47, timezone = pytz.timezone('Asia/Kolkata'))

        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(init_data, every_day_at_time ,id='load_new_data', jobstore='default', replace_existing=True)
        scheduler.start()

        self.stdout.write(self.style.NOTICE('Started scheduler'))
