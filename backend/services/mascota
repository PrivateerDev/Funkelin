from flask import abort
from backend.models import db  # ✅ Importa db correctamente desde `models`
from backend.models.mascota import Mascota

def agregar_mascota(nombre: str, tipo: str, edad: int) -> Mascota:
    """Agrega una nueva mascota a la base de datos con validaciones defensivas."""
    
    # ✅ Precondiciones: Validar entrada antes de procesar
    assert isinstance(nombre, str) and nombre.strip(), "El nombre debe ser un string válido."
    assert isinstance(tipo, str) and tipo.strip(), "El tipo debe ser un string válido."
    assert isinstance(edad, int) and edad > 0, "La edad debe ser un número entero positivo."

    nombre = nombre.strip()
    tipo = tipo.strip()

    nueva_mascota = Mascota(nombre=nombre, tipo=tipo, edad=edad)

    try:
        # ✅ Asegurar contexto de aplicación con manejo de errores
        with db.session.begin():
            db.session.add(nueva_mascota)
            db.session.commit()  # ✅ Confirmar la transacción
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error al guardar la mascota en la base de datos: {str(e)}")

    # ✅ Postcondición: La mascota debe haberse guardado correctamente
    assert nueva_mascota.id is not None, "La mascota no se guardó correctamente en la base de datos."
    
    return nueva_mascota

def obtener_mascotas() -> list[dict]:
    """Devuelve la lista de mascotas con validaciones de integridad."""
    
    try:
        with db.session.no_autoflush:  # ✅ Evitar problemas de concurrencia
            mascotas = Mascota.query.all()
            assert isinstance(mascotas, list), "Error interno: La consulta de mascotas no devolvió una lista."

            return [mascota.to_dict() for mascota in mascotas]

    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error al obtener la lista de mascotas: {str(e)}")

def eliminar_mascota(id: int) -> bool:
    """Elimina una mascota de la base de datos con validaciones robustas."""
    
    # ✅ Precondiciones: Validar el ID
    assert isinstance(id, int) and id > 0, "El ID debe ser un número entero positivo."

    mascota = Mascota.query.get(id)
    if mascota is None:
        abort(404, f"No se encontró ninguna mascota con ID: {id}")

    try:
        # ✅ Asegurar contexto y manejo adecuado de la sesión
        with db.session.begin():
            db.session.delete(mascota)
            db.session.commit()  # ✅ Confirmar eliminación

        # ✅ Postcondición: Verificar que la mascota fue eliminada
        assert Mascota.query.get(id) is None, "La mascota no se eliminó correctamente de la base de datos."

        return True
    
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error interno al eliminar la mascota con ID {id}: {str(e)}")