import os
import sys

sys.path.append('instNir/')

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instNir.settings')
app = Celery('instNir')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_data': {
        'task': 'gui_instagram.tasks.update_data_about_users',
        'schedule': crontab(minute='*/15')
    }
}