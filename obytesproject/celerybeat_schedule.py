from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    # Internal tasks
    "delete_messages": {"schedule": crontab(minute=1), "task": "status.tasks.delete_messages"},
}
