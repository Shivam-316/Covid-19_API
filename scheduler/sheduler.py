from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from .setup_db import init_data
from django_apscheduler.jobstores import DjangoJobStore
import sys
import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(init_data, 'cron', day_of_week='mon-fri', hour=23, minute=20, id='load_new_data', jobstore='default', replace_existing=True)
    scheduler.start()