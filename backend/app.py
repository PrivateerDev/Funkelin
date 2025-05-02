"""
Este módulo contiene la configuración principal de la aplicación Flask
y define las rutas iniciales de Funkelin Robusto.
"""

import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.models import db
from backend.models.mascota import Mascota

# ✅ Configurar logging para auditoría y detección de errores
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ✅ Configuración segura de la aplicación Flask
app = Flask(__name__)

# ✅ Obtener la URI de la base de datos desde variables de entorno
DATABASE_PATH = os.getenv("DATABASE_PATH", "backend/mascotas.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(DATABASE_PATH)}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Inicializar la base de datos con la aplicación Flask
db.init_app(app)

# ✅ Habilitar CORS con control refinado de accesos
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})

# ✅ Registrar rutas después de inicializar `app` y `db`
from backend.routes.mascotas import mascotas_bp
app.register_blueprint(mascotas_bp)

# ✅ Crear tablas dentro del contexto de Flask con manejo seguro de errores
with app.app_context():
    try:
        db.create_all()
        logging.info(f"✅ Base de datos inicializada en: {os.path.abspath(DATABASE_PATH)}")
    except Exception as e:
        logging.error(f"⚠ Error al inicializar la base de datos: {str(e)}")

# ✅ Ruta principal
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido a Funkelin API Modularizado 🚀"}), 200

# ✅ Ruta de depuración con validación de conexión
@app.route("/api/debug", methods=["GET"])
def debug():
    """Consulta todos los objetos Mascota registrados en la base de datos con manejo seguro."""
    try:
        with app.app_context():
            if not db.session.is_active:
                raise RuntimeError("⚠ La conexión con la base de datos no está activa.")

            mascotas = Mascota.query.all()
            if not mascotas:
                return jsonify({"mensaje": "No hay mascotas registradas."}), 404
            
            return jsonify([m.to_dict() for m in mascotas]), 200
    except RuntimeError as re:
        logging.error(f"⚠ Error de conexión: {str(re)}")
        return jsonify({"error": f"Error de conexión a la base de datos: {str(re)}"}), 500
    except Exception as e:
        logging.error(f"⚠ Error en `debug()`: {str(e)}")
        return jsonify({"error": f"Error al consultar mascotas: {str(e)}"}), 500

# ✅ Ejecutar la aplicación en modo seguro con control de entorno
if __name__ == "__main__":
    flask_env = os.getenv("FLASK_ENV", "development")
    logging.info(f"🚀 Iniciando Funkelin API en modo: {flask_env}")
    app.run(debug=(flask_env == "development"))