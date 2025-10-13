from flask import Blueprint, request, jsonify
from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Registro de usuario
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username y password requeridos"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Usuario ya existe"}), 400

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente"})


# Login de usuario
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username y password requeridos"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    return jsonify({
        "message": "Login correcto",
        "user_id": user.id,
        "is_admin": user.is_admin
    })

