import os
import sys

sys.path.append('config/')

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_data': {
        'task': 'data_processing.tasks.update_data_about_users',
        'schedule': crontab(hour='*/1')
    }
}