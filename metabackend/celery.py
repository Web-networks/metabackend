import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metabackend.settings')

app = Celery('metabackend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
