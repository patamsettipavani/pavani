from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/register", methods=["POST"])
def register():
    # Get JSON data safely
    data = request.get_json(silent=True)
    
    # Strict check: data MUST be a dictionary (JSON object), not a string or None
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid request. Body must be a valid JSON object."}), 400

    username = str(data.get("username") or "").strip()
    email = str(data.get("email") or "").strip()
    password = str(data.get("password") or "")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "username, email, and password are required."}), 400

    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters."}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"success": False, "message": "Username or email already exists."}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "token": token,
        "user": {"id": user.id, "username": user.username, "email": user.email},
    }), 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid request. Body must be a valid JSON object."}), 400

    email = str(data.get("email") or "").strip()
    password = str(data.get("password") or "")

    if not email or not password:
        return jsonify({"success": False, "message": "email and password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "success": True,
        "token": token,
        "user": {"id": user.id, "username": user.username, "email": user.email},
    }), 200