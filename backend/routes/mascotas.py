import re
import logging
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from backend.models import db
from backend.models.mascota import Mascota
from backend.services.mascota_service import agregar_mascota, obtener_mascotas

# ✅ Configurar logging con múltiples niveles para trazabilidad completa
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_routes.log", encoding="utf-8"),  # Asegurar codificación
        logging.StreamHandler()
    ]
)

# ✅ Definir el blueprint con un prefijo estructurado
logging.debug("Inicializando Blueprint para mascotas")
mascotas_bp = Blueprint("mascotas", __name__, url_prefix="/api/mascotas")
CORS(mascotas_bp, resources={r"/api/*": {"origins": "*"}})

# ✅ Diccionario centralizado de errores
ERROR_MESSAGES = {
    "no_data": "No se recibió ningún dato.",
    "invalid_age": "Edad debe ser un número entero positivo.",
    "invalid_name": "El nombre debe contener solo letras y espacios, sin números ni símbolos.",
    "name_as_url": "El nombre no puede ser un enlace. Introduce un nombre válido sin direcciones web.",
    "invalid_type": "Tipo de mascota no válido.",
    "unexpected_error": "Error interno inesperado.",
    "mascota_not_found": "Mascota no encontrada."
}

# ✅ Expresión regular para detectar URLs
URL_REGEX = re.compile(r"^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$")

# ✅ Ruta de prueba para verificar conexión
@mascotas_bp.route("/test", methods=["GET"])
def test():
    logging.info("Endpoint `/test` ejecutado correctamente")
    return jsonify({"mensaje": "Funkelin backend activo 🚀"}), 200

# ✅ Función para sanitizar texto de entrada
def sanitizar_texto(texto: str) -> str:
    """Elimina caracteres peligrosos y espacios extra para prevenir XSS."""
    logging.debug(f"Sanitizando texto: {texto}")
    return re.sub(r'[<>"\'&]', '', texto).strip()

# ✅ Ruta para agregar una nueva mascota con programación defensiva
@mascotas_bp.route("/", methods=["POST"])
def post_mascota():
    logging.debug("Ejecutando `post_mascota()`")
    try:
        data = request.get_json()
        if not data:
            logging.warning("⚠ Intento de POST sin datos")
            return jsonify({"error": ERROR_MESSAGES["no_data"]}), 400

        nombre = sanitizar_texto(data.get("nombre", ""))
        tipo = sanitizar_texto(data.get("tipo", ""))
        edad = data.get("edad")

        try:
            edad = int(edad)
        except ValueError:
            logging.warning("⚠ Edad no válida en `post_mascota()`")
            return jsonify({"error": ERROR_MESSAGES["invalid_age"]}), 400

        # ✅ **Verificar si el nombre es una URL antes de hacer más validaciones**
        if URL_REGEX.match(nombre):
            logging.warning(f"⚠ Se detectó una URL en lugar de un nombre: {nombre}")
            return jsonify({"error": ERROR_MESSAGES["name_as_url"]}), 400

        if not (nombre and 2 <= len(nombre) <= 50):
            logging.warning(f"⚠ Nombre inválido: {nombre}")
            return jsonify({"error": ERROR_MESSAGES["invalid_name"]}), 400

        if tipo not in ["Perro", "Gato", "Ave", "Otro"]:
            logging.warning(f"⚠ Tipo inválido: {tipo}")
            return jsonify({"error": ERROR_MESSAGES["invalid_type"]}), 400

        if not (isinstance(edad, int) and edad > 0):
            logging.warning(f"⚠ Edad inválida: {edad}")
            return jsonify({"error": ERROR_MESSAGES["invalid_age"]}), 400

        nueva_mascota = agregar_mascota(nombre, tipo, edad)
        if nueva_mascota is None:
            raise ValueError("Error: La mascota no se creó correctamente.")

        logging.info(f"✅ Mascota agregada: {nueva_mascota.to_dict()}")
        return jsonify(nueva_mascota.to_dict()), 201
    except (AssertionError, ValueError) as ae:
        logging.warning(f"⚠ Validación fallida en `post_mascota()`: {str(ae)}")
        return jsonify({"error": str(ae)}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"⚠ Error crítico en `post_mascota()`: {str(e)}")
        return jsonify({"error": ERROR_MESSAGES["unexpected_error"]}), 500

# ✅ Ruta para obtener todas las mascotas con manejo de errores
@mascotas_bp.route("/", methods=["GET"])
def get_mascotas():
    logging.debug("Ejecutando `get_mascotas()`")
    try:
        mascotas = obtener_mascotas()
        assert isinstance(mascotas, list), "La respuesta debe ser una lista."

        logging.info(f"Mascotas obtenidas exitosamente ({len(mascotas)} registros)")
        return jsonify(mascotas), 200
    except AssertionError as ae:
        logging.error(f"Error en `get_mascotas()`: {str(ae)}")
        return jsonify({"error": ERROR_MESSAGES["unexpected_error"]}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error crítico en `get_mascotas()`: {str(e)}")
        return jsonify({"error": ERROR_MESSAGES["unexpected_error"]}), 500

# ✅ Ruta para eliminar una mascota con control de errores
@mascotas_bp.route("/<int:mascota_id>", methods=["DELETE"])
def eliminar_mascota(mascota_id):
    logging.debug(f"Ejecutando `eliminar_mascota()` con ID {mascota_id}")
    try:
        mascota = Mascota.query.get(mascota_id)
        if not mascota:
            logging.warning(f"⚠ Intento de eliminación de mascota no existente (ID {mascota_id})")
            return jsonify({"error": ERROR_MESSAGES["mascota_not_found"]}), 404

        db.session.delete(mascota)
        db.session.commit()

        logging.info(f"✅ Mascota eliminada: ID {mascota_id}")
        return jsonify({"mensaje": f"Mascota con ID {mascota_id} eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"⚠ Error en `eliminar_mascota()`: {str(e)}")
        return jsonify({"error": ERROR_MESSAGES["unexpected_error"]}), 500