import logging

# ✅ Configurar logging para la inicialización de servicios
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_services_init.log"),
        logging.StreamHandler()
    ]
)

logging.debug("🔄 Iniciando la importación de servicios en `services/__init__.py`")

# ✅ Diccionario centralizado de errores
ERROR_MESSAGES = {
    "import_fail": "No se pudo importar los servicios. Verifica rutas o dependencias.",
    "unexpected_error": "Error inesperado en la inicialización de servicios."
}

# ✅ Importación organizada de servicios
try:
    from backend.services.mascota_service import agregar_mascota, obtener_mascotas, eliminar_mascota  # noqa: F401
    logging.info("✅ Servicios importados correctamente: `agregar_mascota`, `obtener_mascotas`, `eliminar_mascota`")
except ImportError as e:
    logging.error(f"⚠ {ERROR_MESSAGES['import_fail']} - Detalles: {e}")

# ✅ Registro global de servicios
__all__ = ["agregar_mascota", "obtener_mascotas", "eliminar_mascota"]

logging.debug("✅ Finalizando la inicialización de `services/__init__.py`")