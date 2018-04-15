import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sliply_project.settings')

app = Celery('sliply_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
