# ✅ Importación organizada de servicios
from backend.services.mascota_service import agregar_mascota, obtener_mascotas, eliminar_mascota  # noqa: F401

# ✅ Registro global de servicios
__all__ = ["agregar_mascota", "obtener_mascotas", "eliminar_mascota"]