# mascota_service.py
from flask import abort
from backend.models import db  # ✅ Importa db correctamente desde `models`
from backend.models.mascota import Mascota

def agregar_mascota(nombre: str, tipo: str, edad: int) -> Mascota:
    """Agrega una nueva mascota a la base de datos."""
    # Validar datos de entrada
    if not nombre.strip() or not tipo.strip() or edad <= 0:
        raise ValueError("Los datos proporcionados son inválidos: nombre, tipo y edad son requeridos y deben ser válidos.")

    # Crear una nueva instancia de Mascota
    nueva_mascota = Mascota(nombre=nombre, tipo=tipo, edad=edad)

    # ✅ Asegurar contexto de aplicación
    with db.session.begin():
        db.session.add(nueva_mascota)
        db.session.commit()  # ✅ Confirmar la transacción

    return nueva_mascota

def obtener_mascotas() -> list[dict]:
    """Devuelve la lista de mascotas como una lista de diccionarios."""
    with db.session.no_autoflush:  # ✅ Evitar problemas de concurrencia
        return [mascota.to_dict() for mascota in Mascota.query.all()]

def eliminar_mascota(id: int) -> bool:
    """Elimina una mascota de la base de datos por su ID."""
    if id <= 0:
        abort(400, "El ID proporcionado no es válido.")

    mascota = Mascota.query.get(id)
    if mascota is None:
        abort(404, f"No se encontró ninguna mascota con ID: {id}")

    # ✅ Asegurar contexto y gestión adecuada de la sesión
    with db.session.begin():
        db.session.delete(mascota)
        db.session.commit()  # ✅ Confirmar eliminación en la base de datos

    return True
