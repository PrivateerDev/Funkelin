import logging
from flask_sqlalchemy import SQLAlchemy

# ✅ Configurar logging para auditoría de inicialización de base de datos
logging.basicConfig(
    level=logging.DEBUG,  # Permitimos rastreo completo
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_db.log", encoding="utf-8"),  # Asegurar codificación UTF-8
        logging.StreamHandler()
    ]
)

logging.debug("🔄 Inicializando la instancia de SQLAlchemy")

# ✅ Diccionario centralizado de errores
ERROR_MESSAGES = {
    "import_fail": "No se pudo importar el modelo Mascota. Verifica rutas o dependencias.",
    "unexpected_error": "Error inesperado en la inicialización de la base de datos."
}

# ✅ Inicialización segura de la base de datos
try:
    db = SQLAlchemy()
    logging.info("✅ Base de datos inicializada correctamente")
except Exception as e:
    logging.critical(f"⚠ {ERROR_MESSAGES['unexpected_error']} - Detalles: {e}")
    raise RuntimeError(ERROR_MESSAGES["unexpected_error"])

# ✅ Importación explícita de modelos para evitar errores de referencia circular
logging.debug("🔄 Importando el modelo Mascota")
try:
    from backend.models.mascota import Mascota  # noqa: F401
    logging.info("✅ Modelo `Mascota` importado correctamente")
except ImportError as e:
    logging.error(f"⚠ {ERROR_MESSAGES['import_fail']} - Detalles: {e}")

# ✅ Definir los elementos disponibles en el módulo
__all__ = ["db", "Mascota"]

logging.debug("✅ Finalizando la inicialización del módulo de base de datos")