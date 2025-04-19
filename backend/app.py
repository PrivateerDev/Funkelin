"""
Este módulo contiene la configuración principal de la aplicación Flask
y define las rutas iniciales de Funkelin.
"""

import os  # Import estándar primero

from flask import Flask, jsonify  # Librerías de terceros después
from backend.routes.mascotas import mascotas_bp  # Importaciones del proyecto al final
from backend.models import db  # Importación única de db
from backend.models.mascota import Mascota  # Mover importación al toplevel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mascotas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar SQLAlchemy con Flask
db.init_app(app)

# Imprimir la ubicación de la base de datos
print("Base de datos activa:", os.path.abspath("mascotas.db"))

# Crear tablas en la base de datos
with app.app_context():
    db.create_all()

# Registrar rutas
app.register_blueprint(mascotas_bp)


# Ruta principal
@app.route("/")
def home():
    """Devuelve un mensaje de bienvenida."""
    return "Bienvenido a Funkelin API Modularizado 🚀"


# Ruta de depuración
@app.route("/api/debug", methods=["GET"])
def debug():
    """
    Devuelve una lista de mascotas para depuración.
    Consulta todos los objetos Mascota registrados en la base de datos.
    """
    try:
        mascotas = Mascota.query.all()
        return jsonify([m.to_dict() for m in mascotas]), 200
    except AttributeError as e:
        # Específica para errores de atributos relacionados con Mascota
        return jsonify({"error": f"Error en atributos al consultar mascotas: {str(e)}"}), 500
    except RuntimeError as e:
        # Específica para errores en tiempo de ejecución, como problemas del contexto de la app
        return jsonify({"error": f"Error de ejecución: {str(e)}"}), 500
    except ImportError as e:
        # Específica para problemas de importación
        return jsonify({"error": f"Error al importar: {str(e)}"}), 500


if __name__ == "__main__":
    # Cambiar debug a dinámico basado en la variable de entorno FLASK_ENV
    app.run(debug=os.getenv("FLASK_ENV") == "development")
