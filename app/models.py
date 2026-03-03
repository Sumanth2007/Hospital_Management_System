from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    patient_email = Column(String, nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    mail_sent = Column(Boolean, default=False)