import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoCeleryProject.settings")
app = Celery("djangoCeleryProject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()