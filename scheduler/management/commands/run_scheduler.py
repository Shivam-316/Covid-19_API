from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from scheduler.periodic_tasks import periodically_run_job
import pytz
from apscheduler.triggers.cron import CronTrigger
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
class Command(BaseCommand):
    help = 'Run blocking scheduler to create periodical tasks'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Preparing scheduler'))
        scheduler = BackgroundScheduler(timezone = pytz.timezone('Asia/Kolkata'))
        every_day_at_time = CronTrigger(hour=10, minute=20, timezone = pytz.timezone('Asia/Kolkata'))
        scheduler.add_job(periodically_run_job, every_day_at_time ,id='load_new_data', jobstore='default', replace_existing=True)
        scheduler.start()
        self.stdout.write(self.style.NOTICE('Started scheduler'))