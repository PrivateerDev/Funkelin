"""
Este módulo contiene la configuración principal de la aplicación Flask
y define las rutas iniciales de Funkelin.
"""

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ Importar flask-cors
from backend.models import db  # ✅ Importa db desde models en lugar de definirlo aquí
from backend.models.mascota import Mascota  # ✅ Importar después de que `db` está registrado

print("Base de datos activa:", os.path.abspath("backend/mascotas.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath('backend/mascotas.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Inicializar la base de datos con la aplicación Flask
db.init_app(app)

# ✅ Habilitar CORS para permitir solicitudes desde el frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ✅ Registrar rutas después de inicializar `app` y `db`
from backend.routes.mascotas import mascotas_bp
app.register_blueprint(mascotas_bp)

# ✅ Crear tablas dentro del contexto de Flask
with app.app_context():
    db.create_all()
    print("Ruta de la base de datos:", os.path.abspath("backend/mascotas.db"))

# ✅ Verificar que la base de datos está accesible
with app.app_context():
    try:
        mascotas = Mascota.query.all()
        print("Mascotas en la base de datos:", [m.to_dict() for m in mascotas] if mascotas else "No hay mascotas registradas.")
    except Exception as e:
        print(f"Error al consultar mascotas: {str(e)}")

# ✅ Ruta principal
@app.route("/")
def home():
    return "Bienvenido a Funkelin API Modularizado 🚀"

# ✅ Ruta de depuración
@app.route("/api/debug", methods=["GET"])
def debug():
    """Consulta todos los objetos Mascota registrados en la base de datos."""
    try:
        with app.app_context():
            mascotas = Mascota.query.all()
            if not mascotas:
                return jsonify({"mensaje": "No hay mascotas registradas."}), 404
            return jsonify([m.to_dict() for m in mascotas]), 200
    except Exception as e:
        return jsonify({"error": f"Error al consultar mascotas: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV", "development") == "development")
