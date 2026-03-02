from flask import Blueprint, request, jsonify, current_app
from models import db, User
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    decode_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from jwt.exceptions import ExpiredSignatureError
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER (PATIENT ONLY) ----------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email", "").strip().lower()
    phone = data.get("phone")
    age = data.get("age")
    gender = data.get("gender")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"message": "All required fields are mandatory"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        phone=phone,
        age=age,
        gender=gender,
        password=hashed_password,
        role="patient"
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Patient registered successfully"}), 201


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=20)
    )

    return jsonify({
        "token": access_token,
        "role": user.role,
        "name": user.name
    }), 200


# ---------------- FORGOT PASSWORD ----------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email", "").strip().lower()
    print("FORGOT PASSWORD REQUEST FOR:", email)

    if not email:
        return jsonify({"message": "Email required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email not registered"}), 404

    # Generate reset token (expires in 10 minutes)
    reset_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=10)
    )

    FRONTEND_URL = "http://localhost:8080"
    reset_link = f"{FRONTEND_URL}/reset/{reset_token}"

    sender_email = "hmsproject26@gmail.com"
    sender_password = "lfynpsyxnqvjiypd"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Reset Your Password"

    html_body = f"""
    <html>
      <body>
        <p>Hello,</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_link}" target="_blank">{reset_link}</a></p>
        <p>This link expires in 10 minutes.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return jsonify({"message": "Reset password link sent to email"}), 200

    except Exception as e:
        if (e.strerror == 'getaddrinfo failed'):
            return jsonify({"message": "Some network related error"}), 408
        return jsonify({"message": "Failed to send email"}), 500


# ---------------- RESET PASSWORD ----------------
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("password")

    if not token or not new_password:
        return jsonify({"message": "Token and password required"}), 400

    try:
        decoded_token = decode_token(token)
        user_id = int(decoded_token["sub"])  # identity stored as str

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({"message": "Password reset successful"}), 200

    except ExpiredSignatureError:
        return jsonify({"message": "Reset link expired"}), 400
    except Exception as e:
        print("RESET ERROR:", e)
        return jsonify({"message": "Invalid reset link"}), 400


# ---------------- SESSION CHECK ----------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200
