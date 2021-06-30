from apscheduler.schedulers.background import BackgroundScheduler
from .setup_db import init_data
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
import sys

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(init_data, 'cron', day_of_week='mon-fri', hour=0, minute=0, id='load_new_data', jobstore='default', replace_existing=True)
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)