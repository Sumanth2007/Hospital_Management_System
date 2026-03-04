# app/celery_app.py
from celery import Celery
import os

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "appointment_app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery_app.conf.beat_schedule = {
    "send-appointment-reminders-every-30-seconds": {
        "task": "app.tasks.send_appointment_reminders",
        "schedule": 30.0,
    }
}

celery_app.conf.timezone = "Asia/Kolkata"  # local time for testing