from extensions import db
from datetime import datetime


# Department Table
class Department(db.Model):

    __tablename__ = "departments"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    doctors = db.relationship("Doctor", backref="department", lazy=True)

    def __repr__(self):
        return f"<Department {self.name}>"


# Doctor Table
class Doctor(db.Model):

    __tablename__ = "doctors"

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    email          = db.Column(db.String(120))
    phone          = db.Column(db.String(20))
    availability   = db.Column(db.String(100))
    status         = db.Column(db.String(20), default="available")

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )

    # ✅ Alias so old code using Doctor.dept_id still works
    dept_id = db.synonym("department_id")

    schedules = db.relationship("DoctorSchedule", backref="doctor", lazy=True)

    def __repr__(self):
        return f"<Doctor {self.name}>"


# DoctorSchedule Table — WAS MISSING FROM YOUR models.py, NOW ADDED
class DoctorSchedule(db.Model):

    __tablename__ = "doctor_schedules"

    id        = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    day_of_week = db.Column(db.String(15), nullable=False)  # "Monday", "Tuesday"...
    shift_start = db.Column(db.String(10), default="09:00")
    shift_end   = db.Column(db.String(10), default="17:00")
    work_type   = db.Column(db.String(20), default="OPD")   # OPD/Emergency/Surgery/Leave

    def __repr__(self):
        return f"<DoctorSchedule doctor={self.doctor_id} {self.day_of_week} {self.work_type}>"


class Prescription(db.Model):

    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )
    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )
    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=True
    )

    diagnosis = db.Column(db.String(255), nullable=False)
    medications_json = db.Column(db.Text, nullable=False, default="[]")
    instructions = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="active")

    prescribed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    follow_up_date = db.Column(db.Date, nullable=True)

    doctor = db.relationship("Doctor", backref="prescriptions")
    appointment = db.relationship("Appointment", backref="prescriptions")

    def __repr__(self):
        return f"<Prescription {self.id} patient={self.patient_id} doctor={self.doctor_id}>"
