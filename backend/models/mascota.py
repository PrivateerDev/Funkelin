<<<<<<< HEAD
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
import logging
from backend.models import db  # ✅ Importamos `db`

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

# ✅ Configurar logging con formato detallado y múltiples niveles
logging.basicConfig(
    level=logging.DEBUG,  # Mínimo nivel para registrar todo
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_model.log"),
        logging.StreamHandler()
    ]
)

class Mascota(db.Model):  # type: ignore
    """Modelo de Mascota en la base de datos con validaciones defensivas."""

    __tablename__ = "mascotas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre: str, tipo: str, edad: int) -> None:
        """Inicializa una instancia de Mascota con validaciones seguras."""
        logging.debug("Inicio de la inicialización de Mascota")  # DEBUG

        try:
            self.nombre = self.validar_nombre(nombre)
            self.tipo = self.validar_tipo(tipo)
            self.edad = self.validar_edad(edad)

            logging.info(f"✅ Mascota creada exitosamente: {self.to_dict()}")  # INFO
        except ValueError as e:
            logging.error(f"⚠ Error al crear Mascota: {str(e)}")  # ERROR
            raise

        logging.debug("Fin de la inicialización de Mascota")  # DEBUG

    @staticmethod
    def validar_nombre(nombre: str) -> str:
        """Valida y sanitiza el nombre."""
        logging.debug(f"Validando nombre: {nombre}")
        if not isinstance(nombre, str) or len(nombre.strip()) < 2 or len(nombre.strip()) > 50:
            logging.warning(f"Nombre inválido: {nombre}")  # WARNING
            raise ValueError("⚠ El nombre debe tener entre 2 y 50 caracteres.")
        return nombre.strip()

    @staticmethod
    def validar_tipo(tipo: str) -> str:
        """Valida el tipo de mascota."""
        logging.debug(f"Validando tipo de mascota: {tipo}")
        if not isinstance(tipo, str) or tipo.strip() not in ["Perro", "Gato", "Ave", "Otro"]:
            logging.warning(f"Tipo de mascota inválido: {tipo}")  # WARNING
            raise ValueError("⚠ Tipo de mascota no válido.")
        return tipo.strip()

    @staticmethod
    def validar_edad(edad: int) -> int:
        """Valida la edad como un número entero positivo."""
        logging.debug(f"Validando edad: {edad}")
        if not isinstance(edad, int) or edad <= 0:
            logging.warning(f"Edad inválida: {edad}")  # WARNING
            raise ValueError("⚠ La edad debe ser un número entero positivo.")
        return edad

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto Mascota a un diccionario con tolerancia a errores."""
        logging.debug("Convirtiendo Mascota a diccionario")  # DEBUG
        return {
            "id": getattr(self, "id", None),
            "nombre": getattr(self, "nombre", "Desconocido"),
            "tipo": getattr(self, "tipo", "Desconocido"),
            "edad": getattr(self, "edad", 0)
=======
from models import db  # Importar db desde models/__init__.py

class Mascota(db.Model):
    """Modelo para representar una mascota en la base de datos."""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Convierte la instancia de Mascota a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "edad": self.edad
>>>>>>> f978f38 (Reinstanciación completa del backend:)
        }