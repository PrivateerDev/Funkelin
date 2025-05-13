import logging
from flask import Blueprint

# ✅ Configurar logging para auditoría de importación de rutas
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_routes_init.log"),
        logging.StreamHandler()
    ]
)

logging.debug("Iniciando la importación de Blueprints en `routes/__init__.py`")  # DEBUG

# ✅ Importación organizada de los Blueprints de cada módulo
try:
    from backend.routes.mascotas import mascotas_bp  # noqa: F401
    logging.info("✅ Blueprint `mascotas_bp` importado correctamente")  # INFO
except ImportError as e:
    logging.error(f"⚠ Error al importar `mascotas_bp`: {e}")  # ERROR

# ✅ Registro global de rutas
__all__ = ["mascotas_bp"]

logging.debug("Finalizando la inicialización de `routes/__init__.py`")  # DEBUG