from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
from backend.models import db  # ✅ Ahora sí podemos importar `db` sin problema

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

class Mascota(db.Model):  # type: ignore
    """Modelo de Mascota en la base de datos."""

    __tablename__ = "mascotas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre: str, tipo: str, edad: int) -> None:
        """Inicializa una instancia de Mascota con validaciones."""
        assert isinstance(nombre, str), "El nombre debe ser un string."
        assert len(nombre) > 1, "El nombre debe tener al menos 2 caracteres."
        assert isinstance(tipo, str), "El tipo debe ser un string."
        assert tipo in ["Perro", "Gato", "Ave", "Otro"], "Tipo no válido."
        assert isinstance(edad, int), "La edad debe ser un número entero."
        assert edad > 0, "La edad debe ser mayor a 0."

        self.nombre = nombre.strip()
        self.tipo = tipo.strip()
        self.edad = edad

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto Mascota a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "edad": self.edad,
        }