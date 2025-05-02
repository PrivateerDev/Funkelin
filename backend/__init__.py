from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# ✅ Inicialización global de la base de datos
db = SQLAlchemy()

# ✅ Función para crear y configurar la aplicación Flask
def create_app():
    """Inicializa la aplicación Flask con configuración segura y modular."""
    app = Flask(__name__)

    # ✅ Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///backend/mascotas.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Inicializar extensiones
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ✅ Registrar Blueprints después de inicializar la app
    from backend.routes.mascotas import mascotas_bp
    app.register_blueprint(mascotas_bp)

    # ✅ Crear tablas dentro del contexto de Flask
    with app.app_context():
        db.create_all()

    return app

# ✅ Exponer solo elementos esenciales
__all__ = ["db", "create_app"]