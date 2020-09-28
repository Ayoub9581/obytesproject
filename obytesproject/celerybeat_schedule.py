from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    # Internal tasks
    "delete_messages": {"schedule": crontab(day_of_week='monday'), "task": "status.tasks.delete_messages"},
}
