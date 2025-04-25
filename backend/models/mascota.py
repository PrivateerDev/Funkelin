# models/mascota.py
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
from backend.models import db  # ✅ Importación desde models para evitar ciclos

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

class Mascota(db.Model):  # type: ignore
    __tablename__ = "mascotas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ✅ Agregué autoincrement para evitar problemas de ID manuales
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto Mascota a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "edad": self.edad,
        }
