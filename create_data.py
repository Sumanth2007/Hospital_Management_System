from datetime import datetime, timedelta
from app.database import SessionLocal, engine
from app.models import Base, Appointment

Base.metadata.create_all(bind=engine)

db = SessionLocal()

appt = Appointment(
    patient_name="sneha",
    patient_email="sneharampur7@gmail.com",
    appointment_time=datetime.now() + timedelta(minutes=2),
)

db.add(appt)
db.commit()
db.close()

print("Appointment created successfully")