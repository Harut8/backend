from celery import Celery
from celery.schedules import crontab

app = Celery('birthdays',
             broker="redis://127.0.0.1:6379")# disable UTC so that Celery can use local time

@app.task
def birthdays_today():
    print('hi')
app.conf.beat_schedule = {
    "birthday-task": {
        "task": "birthdays.birthdays_today",
        "schedule": crontab(minute="*/1")
    }
}