from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from routes.auth import auth_bp
from routes.games import games_bp
from routes.orders import orders_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "dev-secret"

    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/health")
    def health():
        return {"status": "API OK"}

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(orders_bp)

    return app

app = create_app()

if __name__ == "__main__":
    from waitress import serve
    print("🚀 Servidor corriendo en http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)
