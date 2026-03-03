import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_user

from extensions import db
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)

# Production-safe defaults with env overrides.
app.config["SECRET_KEY"] = os.getenv("HMS_SECRET_KEY", "your-secret-key-change-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("HMS_DATABASE_URI", "sqlite:///hms.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("HMS_SESSION_SAMESITE", "Lax")
app.config["SESSION_COOKIE_SECURE"] = os.getenv("HMS_SESSION_SECURE", "0") == "1"

# Extensions
db.init_app(app)
allowed_origins = [
    x.strip()
    for x in os.getenv("HMS_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if x.strip()
]
CORS(
    app,
    supports_credentials=True,
    origins=allowed_origins,
)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from models.patient import Patient
    return Patient.query.get(int(user_id))


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    from models.patient import Patient
    user = Patient.query.filter_by(email=email).first()

    if user and user.password == password:  # swap for check_password_hash later
        login_user(user)
        return jsonify({'status': 'success', 'name': user.name})

    return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    from flask_login import logout_user
    logout_user()
    return jsonify({'status': 'success'})


# Blueprints
app.register_blueprint(dashboard_bp)


# Create tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug_mode)
