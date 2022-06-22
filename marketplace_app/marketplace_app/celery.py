from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace_app.settings")

app = Celery("marketplace_app")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "add-daily-offer": {
        "task": "product.tasks.add_daily_offer",
        "schedule": crontab(minute=0, hour=0),
    },
}



