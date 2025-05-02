from flask import Blueprint

# ✅ Importación organizada de los blueprints de cada módulo
from backend.routes.mascotas import mascotas_bp  # noqa: F401

# ✅ Registro global de rutas
__all__ = ["mascotas_bp"]