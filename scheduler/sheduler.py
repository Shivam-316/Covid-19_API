import logging
from apscheduler.schedulers.background import (BackgroundScheduler,BlockingScheduler)
from django_apscheduler.jobstores import DjangoJobStore
from .setup_db import init_data

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(init_data,'cron',hour=23, minute=20, id='load_new_data', jobstore='default', replace_existing=True)
    scheduler.start()
