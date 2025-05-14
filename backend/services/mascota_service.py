import logging
import re
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
        logging.FileHandler("backend/logs/funkelin_services.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# ✅ Diccionario de errores centralizado
ERROR_MESSAGES = {
    "invalid_name": "El nombre debe contener solo letras y espacios, sin números ni símbolos.",
    "invalid_age": "La edad debe ser un número entero entre 2 y 20 años.",
    "invalid_type": "Tipo de mascota no válido.",
    "name_as_url": "El nombre no puede ser un enlace. Introduce un nombre válido sin direcciones web.",
    "db_commit_fail": "Error interno al guardar la mascota.",
    "db_query_fail": "Error interno al obtener la lista de mascotas.",
    "db_delete_fail": "Error interno al eliminar la mascota."
}

# ✅ Patrón para nombres seguros: solo letras y espacios
NOMBRE_REGEX = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,50}$")

# ✅ Expresión regular para detectar URLs
URL_REGEX = re.compile(r"^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$")

def sanitizar_input(texto: str) -> str:
    """Limpia caracteres potencialmente peligrosos del texto."""
    return re.sub(r"[<>{};\"']", "", texto.strip())

def agregar_mascota(nombre: str, tipo: str, edad: int) -> Mascota:
    """Agrega una nueva mascota a la base de datos con validaciones robustas y tolerancia a errores."""
    logging.debug(f"Inicio de `agregar_mascota()` con datos: nombre={nombre}, tipo={tipo}, edad={edad}")

    try:
        nombre = sanitizar_input(nombre)
        tipo = sanitizar_input(tipo)

        if URL_REGEX.match(nombre):
            logging.warning(f"⚠ Se detectó una URL en lugar de un nombre: {nombre}")
            raise ValueError(ERROR_MESSAGES["name_as_url"])

        if not NOMBRE_REGEX.fullmatch(nombre):
            logging.warning(f"⚠ Nombre inválido: {nombre}")
            raise ValueError(ERROR_MESSAGES["invalid_name"])

        if not (1 < edad <= 20):
            logging.warning(f"⚠ Edad inválida: {edad}")
            raise ValueError(ERROR_MESSAGES["invalid_age"])

        if tipo not in ["Perro", "Gato", "Otro"]:
            logging.warning(f"⚠ Tipo inválido: {tipo}")
            raise ValueError(ERROR_MESSAGES["invalid_type"])

        nueva_mascota = Mascota(nombre=nombre, tipo=tipo, edad=edad)

        @retrying.retry(stop_max_attempt_number=3, wait_fixed=2000)
        def commit_mascota():
            with db.session.begin():
                db.session.add(nueva_mascota)
                db.session.commit()

        commit_mascota()

        assert nueva_mascota.id is not None, ERROR_MESSAGES["db_commit_fail"]
        logging.info(f"✅ Mascota agregada exitosamente: {nueva_mascota.to_dict()}")
        return nueva_mascota

    except (AssertionError, ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        logging.error(f"⚠ {ERROR_MESSAGES['db_commit_fail']} - Detalles: {str(e)}")
        raise RuntimeError(f"{ERROR_MESSAGES['db_commit_fail']} - {str(e)}")

def obtener_mascotas() -> list[dict]:
    """Devuelve la lista de mascotas con manejo de concurrencia y tolerancia a errores."""
    logging.debug("Inicio de `obtener_mascotas()`")

    try:
        with db.session.no_autoflush:
            mascotas = Mascota.query.all()
            assert isinstance(mascotas, list), ERROR_MESSAGES["db_query_fail"]

            logging.info(f"✅ Mascotas obtenidas exitosamente ({len(mascotas)} registros)")
            return [mascota.to_dict() for mascota in mascotas]

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"⚠ {ERROR_MESSAGES['db_query_fail']} - Detalles: {str(e)}")
        raise RuntimeError(f"{ERROR_MESSAGES['db_query_fail']} - {str(e)}")

def eliminar_mascota(id: int) -> bool:
    """Elimina una mascota de la base de datos con validaciones avanzadas y manejo seguro de transacción."""
    logging.debug(f"Inicio de `eliminar_mascota()` con ID={id}")

    try:
        if not isinstance(id, int) or id <= 0:
            logging.warning(f"⚠ ID inválido: {id}")
            raise ValueError("El ID debe ser un número entero positivo.")

        mascota = Mascota.query.get(id)
        if mascota is None:
            logging.warning(f"⚠ Intento de eliminar mascota no existente (ID={id})")
            abort(404, f"No se encontró ninguna mascota con ID: {id}")

        @retrying.retry(stop_max_attempt_number=3, wait_fixed=2000)
        def commit_eliminacion():
            with db.session.begin():
                db.session.delete(mascota)
                db.session.commit()

        commit_eliminacion()

        assert Mascota.query.get(id) is None, ERROR_MESSAGES["db_delete_fail"]
        logging.info(f"✅ Mascota eliminada exitosamente: ID {id}")
        return True

    except (AssertionError, ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        logging.error(f"⚠ {ERROR_MESSAGES['db_delete_fail']} - Detalles: {str(e)}")
        raise RuntimeError(f"{ERROR_MESSAGES['db_delete_fail']} - {str(e)}")