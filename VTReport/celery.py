from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from getrep.models import VTReport

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VTReport.settings')

app = Celery('VTReport')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Add a regular task that clears the query database every 24hrs.
@app.on_after_configure.connect
def setup_periodic_tasks(sender):
    # Executes every morning at 4:00 a.m.
    sender.add_periodic_task( # Clear expired db entries
        crontab(hour=4, minute=0),
        VTReport.objects.filter(not is_recent).delete()
    )

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
