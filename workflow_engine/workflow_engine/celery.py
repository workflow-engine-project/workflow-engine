import os
from celery import Celery
from django import setup

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workflow_engine.settings')

# Create Celery object and configure it using the settings from Django.
app = Celery('workflow_engine')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

setup()
