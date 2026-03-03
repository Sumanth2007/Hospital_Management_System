# run this once to create a test user
from app import app
from extensions import db
from models.patient import Patient

with app.app_context():
    test_user = Patient(
        name="Test User",
        email="test@test.com",
        password="1234",
        gender="Male",
        patient_uid="P001"
    )
    db.session.add(test_user)
    db.session.commit()
    print("User created!")