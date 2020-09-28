from obytesproject.celery import app as celery_app

from .models import  Status
import time
import datetime

@celery_app.task
def delete_messages():
    print(Status.objects.all())
    # Status.objects.delete_old_message_over_10_days()


@celery_app.task
def display_every_10_second():
    for i in range(20):
        time.sleep(10)
        print('AYOUB')


# display_every_10_second.delay()
