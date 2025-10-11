from models import db, Order
from app import app

with app.app_context():
    print("Tabla:", Order.__tablename__)
    print("Columnas:")
    for column in Order.__table__.columns:
        print(f" - {column.name} ({column.type})")