from datetime import datetime
from extensions import db   # ✅ fixed: was "from models import db"


class AppointmentStatus:
    BOOKED    = "booked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Appointment(db.Model):

    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"),   nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)

    appointment_datetime = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.String(20), nullable=False, default=AppointmentStatus.BOOKED)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor  = db.relationship("Doctor",  backref="appointments")
    patient = db.relationship("Patient", backref="appointments")

    def __repr__(self):
        return f"<Appointment {self.id}>"