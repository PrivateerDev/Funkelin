from flask_sqlalchemy import SQLAlchemy

# ✅ Inicialización segura de la base de datos
db = SQLAlchemy()

# ✅ Importación explícita de modelos para evitar errores de referencia circular
from backend.models.mascota import Mascota  # noqa: F401

__all__ = ["db", "Mascota"]