from flask import request, jsonify
from auth import auth_bp
from models import User
from extensions import db
from sqlalchemy import text

@auth_bp.route("/api/login", methods=["POST"])

def login_vulnerable():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON payload"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return (
            jsonify({"success": False, "message": "Username and password required"}),
            400,
        )

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = db.session.execute(text(query))
    user = result.fetchone()

    if not user:
        return (
            jsonify({"success": False, "message": "Invalid username or password"}),
            401,
        )

    return (
        jsonify(
            {
                "success": True,
                "message": "Login successful",
                "user": {"username": user.username},
            }
        ),
        200,
    )
