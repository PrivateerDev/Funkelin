import logging
from flask_sqlalchemy import SQLAlchemy

# ✅ Configurar logging para auditoría de inicialización de base de datos
logging.basicConfig(
    level=logging.DEBUG,  # Permitimos rastreo completo
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_db.log"),
        logging.StreamHandler()
    ]
)

# ✅ Inicialización segura de la base de datos
logging.debug("Inicializando la instancia de SQLAlchemy")  # DEBUG
db = SQLAlchemy()
logging.info("✅ Base de datos inicializada correctamente")  # INFO

# ✅ Importación explícita de modelos para evitar errores de referencia circular
logging.debug("Importando el modelo Mascota")  # DEBUG
try:
    from backend.models.mascota import Mascota  # noqa: F401
    logging.info("✅ Modelo Mascota importado correctamente")  # INFO
except ImportError as e:
    logging.error(f"⚠ Error al importar el modelo Mascota: {e}")  # ERROR

__all__ = ["db", "Mascota"]