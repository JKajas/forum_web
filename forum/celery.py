import os
from celery import Celery
from django.conf import settings


'''
Support of celery allows async checking token with beat_schedule task.
Task is performed every second
'''


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum.settings')
app = Celery('forum')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-1-seconds': {
        'task': 'forum_comments.tasks.checkingtoken',
        'schedule': 1.0,
    },
}
app.conf.timezone = 'UTC'



