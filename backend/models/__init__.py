"""Módulo de inicialización para modelos de Funkelin."""

from flask_sqlalchemy import SQLAlchemy

# ✅ Inicializar la base de datos sin importar modelos aún
db = SQLAlchemy()

# ✅ No importa `Mascota` directamente aquí para evitar ciclos
__all__ = ["db"]  # ✅ Solo exporta `db`