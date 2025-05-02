import logging
from flask import abort
from backend.models import db
from backend.models.mascota import Mascota
from sqlalchemy.exc import SQLAlchemyError
import retrying  # ✅ Para reintentos en operaciones críticas

# ✅ Configurar logging para auditoría y detección de errores
logging.basicConfig(level=logging.INFO)

def agregar_mascota(nombre: str, tipo: str, edad: int) -> Mascota:
    """Agrega una nueva mascota a la base de datos con validaciones robustas y tolerancia a errores."""
    try:
        if not isinstance(nombre, str) or len(nombre.strip()) < 2 or len(nombre.strip()) > 50:
            raise ValueError("⚠ El nombre debe tener entre 2 y 50 caracteres.")
        if not isinstance(tipo, str) or tipo.strip() not in ["Perro", "Gato", "Ave", "Otro"]:
            raise ValueError("⚠ Tipo de mascota no válido.")
        if not isinstance(edad, int) or edad <= 0:
            raise ValueError("⚠ La edad debe ser un número entero positivo.")

        nueva_mascota = Mascota(nombre=nombre.strip(), tipo=tipo.strip(), edad=edad)

        # ✅ Intentar la operación con reintento en caso de error
        @retrying.retry(stop_max_attempt_number=3, wait_fixed=2000)
        def commit_mascota():
            with db.session.begin():
                db.session.add(nueva_mascota)
                db.session.commit()

        commit_mascota()

        assert nueva_mascota.id is not None, "⚠ La mascota no se guardó correctamente en la base de datos."
        logging.info(f"✅ Mascota agregada: {nueva_mascota.to_dict()}")

        return nueva_mascota

    except (AssertionError, ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        logging.error(f"⚠ Error en `agregar_mascota()`: {str(e)}")
        raise RuntimeError(f"Error interno al guardar la mascota: {str(e)}")

def obtener_mascotas() -> list[dict]:
    """Devuelve la lista de mascotas con manejo de concurrencia y tolerancia a errores."""
    try:
        with db.session.no_autoflush:
            mascotas = Mascota.query.all()
            assert isinstance(mascotas, list), "⚠ Error interno: La consulta de mascotas no devolvió una lista."

            return [mascota.to_dict() for mascota in mascotas]

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"⚠ Error en `obtener_mascotas()`: {str(e)}")
        raise RuntimeError(f"Error interno al obtener la lista de mascotas: {str(e)}")

def eliminar_mascota(id: int) -> bool:
    """Elimina una mascota de la base de datos con validaciones avanzadas y manejo seguro de transacción."""
    try:
        if not isinstance(id, int) or id <= 0:
            raise ValueError("⚠ El ID debe ser un número entero positivo.")

        mascota = Mascota.query.get(id)
        if mascota is None:
            abort(404, f"No se encontró ninguna mascota con ID: {id}")

        # ✅ Reintentos en la operación de eliminación
        @retrying.retry(stop_max_attempt_number=3, wait_fixed=2000)
        def commit_eliminacion():
            with db.session.begin():
                db.session.delete(mascota)
                db.session.commit()

        commit_eliminacion()

        assert Mascota.query.get(id) is None, "⚠ La mascota no se eliminó correctamente de la base de datos."
        logging.info(f"✅ Mascota eliminada: ID {id}")

        return True

    except (AssertionError, ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        logging.error(f"⚠ Error en `eliminar_mascota()`: {str(e)}")
        raise RuntimeError(f"Error interno al eliminar la mascota con ID {id}: {str(e)}")