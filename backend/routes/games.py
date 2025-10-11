from flask import Blueprint, request, jsonify
from models import db, Game, User  # agregamos User para comprobar admin

games_bp = Blueprint("games", __name__, url_prefix="/games")

# -------------------------------
# 📌 Listar todos los juegos
# -------------------------------
@games_bp.get("/")
def get_games():
    games = Game.query.all()
    return jsonify([
        {
            "id": game.id,
            "title": game.title,
            "description": game.description,
            "price": game.price,
            "stock": game.stock
        }
        for game in games
    ])

# -------------------------------
# 📌 Obtener un juego por ID
# -------------------------------
@games_bp.get("/<int:game_id>")
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify({
        "id": game.id,
        "title": game.title,
        "description": game.description,
        "price": game.price,
        "stock": game.stock
    })

# -------------------------------
# 📌 Crear un nuevo juego (solo admin)
# -------------------------------
@games_bp.post("/")
def create_game():
    data = request.get_json()
    user_id = data.get("user_id")  # ID del usuario que crea el juego
    title = data.get("title")
    description = data.get("description", "")
    price = data.get("price")
    stock = data.get("stock", 0)

    if not user_id or not title or price is None:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({"error": "No tienes permiso para crear juegos"}), 403

    game = Game(title=title, description=description, price=price, stock=stock)
    db.session.add(game)
    db.session.commit()

    return jsonify({
        "message": "Juego creado correctamente",
        "game": {
            "id": game.id,
            "title": game.title,
            "description": game.description,
            "price": game.price,
            "stock": game.stock
        }
    }), 201

# -------------------------------
# 📌 Editar un juego existente
# -------------------------------
@games_bp.put("/<int:game_id>")
def update_game(game_id):
    game = Game.query.get_or_404(game_id)
    data = request.get_json()

    game.title = data.get("title", game.title)
    game.description = data.get("description", game.description)
    game.price = data.get("price", game.price)
    game.stock = data.get("stock", game.stock)

    db.session.commit()
    return jsonify({"message": "Juego actualizado correctamente"})

# -------------------------------
# 📌 Eliminar un juego
# -------------------------------
@games_bp.delete("/<int:game_id>")
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({"message": "Juego eliminado correctamente"})
