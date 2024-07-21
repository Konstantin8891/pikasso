import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rent.settings")

app = Celery("rent")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(result_expires=3600, enable_utc=True, timezone="Europe/Moscow")

app.autodiscover_tasks()
