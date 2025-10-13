from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from routes.auth import auth_bp
from routes.games import games_bp
from routes.orders import orders_bp
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="static")
    CORS(app)

    # Configuración de base de datos y secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "dev-secret"

    # Inicializar SQLAlchemy y Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Ruta de salud
    @app.get("/health")
    def health():
        return {"status": "API OK"}

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(orders_bp)

    # -------------------------------
    # Servir React desde static
    # -------------------------------
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        # Si el archivo existe en static, servirlo
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        # Si no, servir index.html (React)
        return send_from_directory(app.static_folder, "index.html")

    return app

# Instanciar app
app = create_app()

if __name__ == "__main__":
    from waitress import serve
    print("🚀 Servidor corriendo en http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)

