<<<<<<< HEAD
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# ✅ Configurar logging para la inicialización del backend
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_backend_init.log"),
        logging.StreamHandler()
    ]
)

logging.debug("Iniciando la configuración del backend en `__init__.py`")  # DEBUG

# ✅ Inicialización global de la base de datos
db = SQLAlchemy()
logging.info("✅ Instancia global de SQLAlchemy creada")  # INFO

# ✅ Función para crear y configurar la aplicación Flask
def create_app():
    """Inicializa la aplicación Flask con configuración segura y modular."""
    logging.debug("Creando la aplicación Flask")  # DEBUG

    app = Flask(__name__)

    # ✅ Configuración de la base de datos
    logging.debug("Configurando la base de datos SQLite")  # DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///backend/mascotas.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Inicializar extensiones
    db.init_app(app)
    logging.info("✅ Base de datos inicializada con la aplicación Flask")  # INFO
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    logging.info("✅ CORS configurado correctamente")  # INFO

    # ✅ Registrar Blueprints después de inicializar la app
    try:
        from backend.routes.mascotas import mascotas_bp
        app.register_blueprint(mascotas_bp)
        logging.info("✅ Blueprint `mascotas_bp` registrado exitosamente")  # INFO
    except ImportError as e:
        logging.error(f"⚠ Error al registrar `mascotas_bp`: {e}")  # ERROR

    # ✅ Crear tablas dentro del contexto de Flask
    logging.debug("Creando tablas en la base de datos")  # DEBUG
    with app.app_context():
        try:
            db.create_all()
            logging.info("✅ Tablas creadas exitosamente")  # INFO
        except Exception as e:
            logging.error(f"⚠ Error al crear tablas en la base de datos: {e}")  # ERROR

    logging.debug("Finalizando configuración de la aplicación Flask")  # DEBUG
    return app

# ✅ Exponer solo elementos esenciales
__all__ = ["db", "create_app"]
logging.debug("Finalizando inicialización de `__init__.py`")  # DEBUG
=======
 
>>>>>>> f978f38 (Reinstanciación completa del backend:)
