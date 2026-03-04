from app.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "check-appointments-every-30-seconds": {
        "task": "app.tasks.send_appointment_reminders",
        "schedule": 30.0,
    },
}