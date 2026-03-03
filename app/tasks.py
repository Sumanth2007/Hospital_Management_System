# app/tasks.py
from datetime import datetime, timedelta
from app.celery_app import celery_app
from app.mail import send_email
from app.data_store import appointments

@celery_app.task(name="app.tasks.send_appointment_reminders")
def send_appointment_reminders():
    now = datetime.now()
    reminder_time = now + timedelta(minutes=1)
    print(f"[DEBUG] Now={now}, Reminder Time={reminder_time}")

    for appt in appointments:
        print(f"[DEBUG] Checking {appt['patient_name']} at {appt['appointment_time']}")
        if not appt["mail_sent"] and appt["appointment_time"] <= reminder_time:
            try:
                send_email(
                    appt["patient_email"],
                    "Appointment Reminder",
                    # f"Hi {appt['patient_name']}, your appointment is at {appt['appointment_time'].strftime('%H:%M')}"
                    f"""
                    Hello {appt['patient_name']},

                    This is a friendly reminder that you have an upcoming appointment scheduled on 
                    {appt['appointment_time'].strftime('%A, %B %d, %Y at %I:%M %p')}.

                    Please make sure to arrive a few minutes early. If you need to reschedule or have any questions, 
                    feel free to contact us.

                    Thank you,
                    HMS
                    """
                )
                appt["mail_sent"] = True
                print(f"[INFO] Reminder sent to {appt['patient_email']}")
            except Exception as e:
                print(f"[ERROR] Failed to send email to {appt['patient_email']}: {e}")