import update

# put backin Procfile: web: gunicorn app:app --log-file=-
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def disable_interval():
    sched.remove_job('INTERVAL_JOB')

def enable_interval():
    sched.add_job(update.updateHtaccess(), 'interval', minutes=1, id='INTERVAL_JOB')

sched.start()
sched.add_job(enable_interval, 'cron', day_of_week='thu')
sched.add_job(disable_interval, 'cron', day_of_week='sat')