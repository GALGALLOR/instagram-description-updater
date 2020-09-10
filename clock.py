import update
from apscheduler.schedulers.blocking import BlockingScheduler

# put backin Procfile: web: gunicorn app:app --log-file=-

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='wed', hour=23)
def enable_interval():
    sched.add_job(update.updateHtaccess(), 'interval', minutes=1, id='INTERVAL_JOB')

@sched.scheduled_job('cron', day_of_week='sat', hour=1)
def disable_interval():
    sched.remove_job('INTERVAL_JOB')

sched.start()
print "Scheduler started"

while __name__ == '__main__':
  pass