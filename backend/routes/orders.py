from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem, Game, User

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

# -----------------------------
# Función interna para cambiar estado de un pedido
# -----------------------------
def change_order_status(order, new_status):
    allowed_statuses = ["pending", "paid", "shipped", "cancelled"]
    if new_status not in allowed_statuses:
        return {"error": f"Estado inválido. Valores permitidos: {allowed_statuses}"}, 400

    if new_status == "cancelled" and order.status == "shipped":
        return {"error": "No se puede cancelar un pedido ya enviado"}, 400

    # Restaurar stock si se cancela
    if new_status == "cancelled":
        for item in order.items:
            game = Game.query.get(item.game_id)
            if game:
                game.stock += item.quantity

    order.status = new_status
    db.session.commit()
    return {"message": f"Estado del pedido actualizado a {new_status}", "order_id": order.id, "status": order.status}, 200


# -----------------------------
# Crear un nuevo pedido
# -----------------------------
@orders_bp.post("/")
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    items = data.get("items")  # Lista de {game_id, quantity}

    if not user_id or not items:
        return jsonify({"error": "user_id e items son requeridos"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    order_items = []
    total = 0.0

    for item in items:
        game_id = item.get("game_id")
        quantity = item.get("quantity", 1)

        game = Game.query.get(game_id)
        if not game:
            return jsonify({"error": f"Juego con id {game_id} no encontrado"}), 404
        if game.stock < quantity:
            return jsonify({"error": f"Stock insuficiente para el juego {game.title}"}), 400

        price = game.price * quantity
        total += price
        game.stock -= quantity

        order_items.append(OrderItem(game_id=game.id, quantity=quantity, price=price))

    order = Order(user_id=user.id, total=total, status="pending", items=order_items)
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Pedido creado correctamente", "order_id": order.id, "status": order.status})


# -----------------------------
# Listar pedidos de un usuario
# -----------------------------
@orders_bp.get("/user/<int:user_id>")
def list_orders(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    orders = Order.query.filter_by(user_id=user.id).all()
    result = [
        {
            "order_id": order.id,
            "created_at": order.created_at,
            "total": order.total,
            "items_count": len(order.items),
            "status": order.status
        }
        for order in orders
    ]

    return jsonify(result)


# -----------------------------
# Detalles de un pedido
# -----------------------------
@orders_bp.get("/details/<int:order_id>")
def order_details(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404

    items = [
        {
            "game_id": item.game_id,
            "game_title": Game.query.get(item.game_id).title,
            "quantity": item.quantity,
            "price": item.price
        }
        for item in order.items
    ]

    return jsonify({
        "order_id": order.id,
        "user_id": order.user_id,
        "created_at": order.created_at,
        "total": order.total,
        "status": order.status,
        "items": items
    })


# -----------------------------
# Eliminar un pedido
# -----------------------------
@orders_bp.delete("/<int:order_id>")
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404

    # Restaurar stock
    for item in order.items:
        game = Game.query.get(item.game_id)
        if game:
            game.stock += item.quantity

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"Pedido {order_id} eliminado correctamente"})


# -----------------------------
# Actualizar estado de un pedido
# -----------------------------
@orders_bp.patch("/status/<int:order_id>")
def update_order_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404

    data = request.get_json()
    new_status = data.get("status")
    result, code = change_order_status(order, new_status)
    return jsonify(result), code


# -----------------------------
# Cancelar un pedido
# -----------------------------
@orders_bp.patch("/cancel/<int:order_id>")
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404

    result, code = change_order_status(order, "cancelled")
    return jsonify(result), code
