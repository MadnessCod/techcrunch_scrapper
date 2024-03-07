from __future__ import absolute_import, unicode_literals

import os
import logging
from celery import Celery, shared_task
from celery.schedules import crontab
from django.conf import settings


logging.basicConfig(filename='celery.log', level=logging.INFO)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechCrunchScrapper.settings')

app = Celery('TechCrunchScrapper', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

app.conf.broker_connection_retry = True

app.config_from_object('django.conf:settings', namespace='CELERY', )

app.autodiscover_tasks()


@shared_task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'daily_scrapper': {
        'task': 'blog.tasks.daily_scrapper',
        'schedule': crontab(minute="0", hour="0"),
    },
}
