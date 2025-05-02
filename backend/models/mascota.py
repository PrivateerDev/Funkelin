from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
import logging
from backend.models import db  # ✅ Ahora sí podemos importar `db` sin problema

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

# ✅ Configurar logging para auditoría y detección de errores
logging.basicConfig(level=logging.INFO)

class Mascota(db.Model):  # type: ignore
    """Modelo de Mascota en la base de datos con validaciones defensivas."""

    __tablename__ = "mascotas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre: str, tipo: str, edad: int) -> None:
        """Inicializa una instancia de Mascota con validaciones seguras."""
        try:
            self.nombre = self.validar_nombre(nombre)
            self.tipo = self.validar_tipo(tipo)
            self.edad = self.validar_edad(edad)

            logging.info(f"✅ Mascota creada: {self.to_dict()}")
        except ValueError as e:
            logging.error(f"⚠ Error al crear Mascota: {str(e)}")
            raise

    @staticmethod
    def validar_nombre(nombre: str) -> str:
        """Valida y sanitiza el nombre."""
        if not isinstance(nombre, str) or len(nombre.strip()) < 2 or len(nombre.strip()) > 50:
            raise ValueError("⚠ El nombre debe tener entre 2 y 50 caracteres.")
        return nombre.strip()

    @staticmethod
    def validar_tipo(tipo: str) -> str:
        """Valida el tipo de mascota."""
        if not isinstance(tipo, str) or tipo.strip() not in ["Perro", "Gato", "Ave", "Otro"]:
            raise ValueError("⚠ Tipo de mascota no válido.")
        return tipo.strip()

    @staticmethod
    def validar_edad(edad: int) -> int:
        """Valida la edad como un número entero positivo."""
        if not isinstance(edad, int) or edad <= 0:
            raise ValueError("⚠ La edad debe ser un número entero positivo.")
        return edad

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto Mascota a un diccionario con tolerancia a errores."""
        return {
            "id": getattr(self, "id", None),
            "nombre": getattr(self, "nombre", "Desconocido"),
            "tipo": getattr(self, "tipo", "Desconocido"),
            "edad": getattr(self, "edad", 0)
        }