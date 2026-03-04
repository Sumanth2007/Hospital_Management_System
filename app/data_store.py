# app/data_store.py
from datetime import datetime, timedelta

# In-memory appointments list
appointments = [
    {
        "patient_name": "sneha",
        "patient_email": "sneharampur7@gmail.com",
        "appointment_time": datetime.now() + timedelta(minutes=1),  # 1 min from now
        "mail_sent": False
    },
    {
        "patient_name": "Alice",
        "patient_email": "sumanthlokesh2000@gmail.com",
        "appointment_time": datetime.now() + timedelta(minutes=2),  # 2 min from now
        "mail_sent": False
    }
]