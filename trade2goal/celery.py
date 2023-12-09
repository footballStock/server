from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trade2goal.settings")

app = Celery("trade2goal",include=["trade2goal.tasks", "team_info.tasks"])
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

app.conf.beat_schedule = {
    "task-every-1-days": {
        "task": "get_news",
        "schedule": 86400,
    },
}


app.autodiscover_tasks()
if __name__ == "__main__":
    app.start()
