<<<<<<< HEAD
import logging
from flask import abort
from backend.models import db
from backend.models.mascota import Mascota
from sqlalchemy.exc import SQLAlchemyError
import retrying  # ✅ Para reintentos en operaciones críticas

# ✅ Configurar logging para auditoría detallada
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_services.log"),
        logging.StreamHandler()
    ]
)

def agregar_mascota(nombre: str, tipo: str, edad: int) -> Mascota:
    """Agrega una nueva mascota a la base de datos con validaciones robustas y tolerancia a errores."""
    logging.debug(f"Inicio de `agregar_mascota()` con datos: nombre={nombre}, tipo={tipo}, edad={edad}")  # DEBUG

    try:
        if not isinstance(nombre, str) or len(nombre.strip()) < 2 or len(nombre.strip()) > 50:
            logging.warning(f"⚠ Nombre inválido en `agregar_mascota()`: {nombre}")  # WARNING
            raise ValueError("El nombre debe tener entre 2 y 50 caracteres.")
        if not isinstance(tipo, str) or tipo.strip() not in ["Perro", "Gato", "Ave", "Otro"]:
            logging.warning(f"⚠ Tipo inválido en `agregar_mascota()`: {tipo}")  # WARNING
            raise ValueError("Tipo de mascota no válido.")
        if not isinstance(edad, int) or edad <= 0:
            logging.warning(f"⚠ Edad inválida en `agregar_mascota()`: {edad}")  # WARNING
            raise ValueError("La edad debe ser un número entero positivo.")

        nueva_mascota = Mascota(nombre=nombre.strip(), tipo=tipo.strip(), edad=edad)

        # ✅ Intentar la operación con reintento en caso de error
        @retrying.retry(stop_max_attempt_number=3, wait_fixed=2000)
        def commit_mascota():
            with db.session.begin():
                db.session.add(nueva_mascota)
                db.session.commit()

        commit_mascota()

        assert nueva_mascota.id is not None, "⚠ La mascota no se guardó correctamente en la base de datos."
        logging.info(f"✅ Mascota agregada exitosamente: {nueva_mascota.to_dict()}")  # INFO

        return nueva_mascota

    except (AssertionError, ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        logging.error(f"⚠ Error crítico en `agregar_mascota()`: {str(e)}")  # ERROR
        raise RuntimeError(f"Error interno al guardar la mascota: {str(e)}")

def obtener_mascotas() -> list[dict]:
    """Devuelve la lista de mascotas con manejo de concurrencia y tolerancia a errores."""
    logging.debug("Ejecutando `obtener_mascotas()`")  # DEBUG

    try:
        with db.session.no_autoflush:
            mascotas = Mascota.query.all()
            assert isinstance(mascotas, list), "⚠ La consulta de mascotas no devolvió una lista."

            logging.info(f"✅ Mascotas obtenidas exitosamente ({len(mascotas)} registros)")  # INFO
            return [mascota.to_dict() for mascota in mascotas]

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"⚠ Error crítico en `obtener_mascotas()`: {str(e)}")  # ERROR
        raise RuntimeError(f"Error interno al obtener la lista de mascotas: {str(e)}")

def eliminar_mascota(id: int) -> bool:
    """Elimina una mascota de la base de datos con validaciones avanzadas y manejo seguro de transacción."""
    logging.debug(f"Ejecutando `eliminar_mascota()` con ID={id}")  # DEBUG

    try:
        if not isinstance(id, int) or id <= 0:
            logging.warning(f"⚠ ID inválido en `eliminar_mascota()`: {id}")  # WARNING
            raise ValueError("El ID debe ser un número entero positivo.")

        mascota = Mascota.query.get(id)
        if mascota is None:
            logging.warning(f"⚠ Intento de eliminar mascota no existente (ID={id})")  # WARNING
            abort(404, f"No se encontró ninguna mascota con ID: {id}")

        # ✅ Reintentos en la operación de eliminación
        @retrying.retry(stop_max_attempt_number=3, wait_fixed=2000)
        def commit_eliminacion():
            with db.session.begin():
                db.session.delete(mascota)
                db.session.commit()

        commit_eliminacion()

        assert Mascota.query.get(id) is None, "⚠ La mascota no se eliminó correctamente de la base de datos."
        logging.info(f"✅ Mascota eliminada exitosamente: ID {id}")  # INFO

        return True

    except (AssertionError, ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        logging.error(f"⚠ Error crítico en `eliminar_mascota()`: {str(e)}")  # ERROR
        raise RuntimeError(f"Error interno al eliminar la mascota con ID {id}: {str(e)}")
=======
from models.mascota import Mascota, db  # Asegúrate de importar correctamente la base de datos

def agregar_mascota(nombre, tipo, edad):
    """Agrega una nueva mascota a la base de datos."""
    # Crear una nueva instancia de Mascota
    nueva_mascota = Mascota(nombre=nombre, tipo=tipo, edad=edad)
    db.session.add(nueva_mascota)  # Añadir al registro en la base de datos
    db.session.commit()  # Guardar cambios en la base de datos
    return nueva_mascota

def obtener_mascotas():
    """Devuelve la lista completa de mascotas desde la base de datos."""
    # Consultar todas las mascotas en la base de datos
    return Mascota.query.all()

def eliminar_mascota(id):
    """Elimina una mascota de la base de datos por su ID."""
    # Buscar la mascota por ID
    mascota = Mascota.query.get(id)
    if mascota is None:
        raise ValueError(f"No se encontró ninguna mascota con ID: {id}")
    db.session.delete(mascota)  # Eliminar el registro de la base de datos
    db.session.commit()  # Guardar cambios en la base de datos
    return True
>>>>>>> f978f38 (Reinstanciación completa del backend:)
