from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import bcrypt

db = SQLAlchemy()

# -------------------------------
# 📌 Modelo de Usuario
# -------------------------------
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str):
        """Hashea la contraseña usando bcrypt."""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica la contraseña."""
        return bcrypt.verify(password, self.password_hash)

# -------------------------------
# 📌 Modelo de Juego
# -------------------------------
class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

# -------------------------------
# 📌 Modelo de Pedido
# -------------------------------
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(20), default="pending")  # pending, paid, shipped
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

# -------------------------------
# 📌 Items de Pedido
# -------------------------------
class OrderItem(db.Model):
    __tablename__ = "order_item"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # precio unitario en el momento del pedido
