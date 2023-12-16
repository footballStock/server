from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trade2goal.settings")

# Create an instance of the Celery application.
app = Celery("trade2goal", include=["trade2goal.tasks", "team_info.tasks"])
# Load configuration from the Django settings, using a prefix of 'CELERY'.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    CELERY_TASK_SERIALIZER="json",
    CELERY_ACCEPT_CONTENT=["json"],
    CELERY_RESULT_SERIALIZER="json",
    CELERY_TIMEZONE="Asia/Seoul",
    CELERY_ENABLE_UTC=False,
    CELERY_BEAT_SCHEDULER="django_celery_beat.schedulers:DatabaseScheduler",
    CELERY_TASK_TRACK_STARTED=True,
    CELERY_TASK_TIME_LIMIT=30 * 60,
)

# Define a periodic task with Celery beat.
app.conf.beat_schedule = {
    "task-every-1-days": {  # Name of the task.
        "task": "get_news",  # Task function to be scheduled.
        "schedule": 86400,  # Schedule task every 86400 seconds (1 day).
    },
}


app.autodiscover_tasks()
if __name__ == "__main__":
    app.start()
