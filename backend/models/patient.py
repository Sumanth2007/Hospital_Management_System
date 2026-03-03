from models import db
from flask_login import UserMixin

class Patient(db.Model,UserMixin):

    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    patient_uid = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)