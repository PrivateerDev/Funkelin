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

logging.debug("🔄 Iniciando la configuración del backend en `__init__.py`")

# ✅ Diccionario centralizado de errores
ERROR_MESSAGES = {
    "import_fail": "No se pudo registrar el Blueprint `mascotas_bp`. Verifica rutas o dependencias.",
    "db_create_fail": "Error al crear las tablas en la base de datos.",
    "unexpected_error": "Error inesperado en la inicialización del backend."
}

# ✅ Inicialización global de la base de datos
try:
    db = SQLAlchemy()
    logging.info("✅ Instancia global de SQLAlchemy creada")
except Exception as e:
    logging.critical(f"⚠ {ERROR_MESSAGES['unexpected_error']} - Detalles: {e}")
    raise RuntimeError(ERROR_MESSAGES["unexpected_error"])

# ✅ Función para crear y configurar la aplicación Flask
def create_app():
    """Inicializa la aplicación Flask con configuración segura y modular."""
    logging.debug("🔄 Creando la aplicación Flask")

    app = Flask(__name__)

    #