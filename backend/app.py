from flask import Flask, request, jsonify, send_from_directory
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
    app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "dev-secret"

    db.init_app(app)
    migrate.init_app(app, db)

    # Rutas API
    app.register_blueprint(auth_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(orders_bp)

    # Ruta de salud
    @app.get("/health")
    def health():
        return {"status": "API OK"}

    # Servir React
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + "/" + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    return app

app = create_app()

if __name__ == "__main__":
    from waitress import serve
    print("🚀 Servidor corriendo en http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)

