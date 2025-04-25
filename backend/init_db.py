# init_db.py
from backend.models import db
from flask import Flask
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath('backend/mascotas.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Asegurar que `db` está correctamente vinculado
db.init_app(app)

# ✅ Crear la base de datos dentro del contexto de Flask
with app.app_context():
    db.create_all()
    print("Base de datos inicializada correctamente.")
