import logging
from .tasks import init_data

def periodically_run_job():
    """
    This task will be run by APScheduler. It can prepare some data and parameters and then enqueue background task.
    """
    logging.warning('It is time to start the dramatiq task')
    init_data.send()