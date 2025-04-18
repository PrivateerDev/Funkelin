<<<<<<< HEAD
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
        logging.FileHandler("backend/logs/funkelin_routes.log"),
        logging.StreamHandler()
    ]
)

# ✅ Definir el blueprint con un prefijo estructurado
logging.debug("Inicializando Blueprint para mascotas")  # DEBUG
mascotas_bp = Blueprint("mascotas", __name__, url_prefix="/api/mascotas")
CORS(mascotas_bp, resources={r"/api/*": {"origins": "*"}})  # ✅ Evita restricciones innecesarias

# ✅ Ruta de prueba para verificar conexión
@mascotas_bp.route("/test", methods=["GET"])
def test():
    logging.info("✅ Endpoint `/test` ejecutado correctamente")  # INFO
    return jsonify({"mensaje": "Funkelin backend activo 🚀"}), 200

# ✅ Función para sanitizar texto de entrada
def sanitizar_texto(texto: str) -> str:
    """Elimina caracteres peligrosos y espacios extra para prevenir XSS."""
    logging.debug(f"Sanitizando texto: {texto}")  # DEBUG
    texto_limpio = re.sub(r'[<>"\'&]', '', texto).strip()
    return texto_limpio

# ✅ Ruta para obtener todas las mascotas con manejo de errores
@mascotas_bp.route("/", methods=["GET"])
def get_mascotas():
    logging.debug("Ejecutando `get_mascotas()`")  # DEBUG
    try:
        mascotas = obtener_mascotas()
        assert isinstance(mascotas, list), "Error: La respuesta debe ser una lista."

        logging.info(f"✅ Mascotas obtenidas exitosamente ({len(mascotas)} registros)")  # INFO
        return jsonify(mascotas), 200
    except AssertionError as ae:
        logging.error(f"⚠ Error en `get_mascotas()`: {str(ae)}")  # ERROR
        return jsonify({"error": f"Error interno: {str(ae)}"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"⚠ Error crítico en `get_mascotas()`: {str(e)}")  # ERROR
        return jsonify({"error": f"Error al obtener mascotas: {str(e)}"}), 500

# ✅ Ruta para agregar una nueva mascota con programación defensiva
@mascotas_bp.route("/", methods=["POST"])
def post_mascota():
    logging.debug("Ejecutando `post_mascota()`")  # DEBUG
    try:
        data = request.get_json()
        if not data:
            logging.warning("⚠ Intento de POST sin datos")  # WARNING
            return jsonify({"error": "No se recibió ningún dato."}), 400

        # ✅ Sanitización y validaciones de entrada
        nombre = sanitizar_texto(data.get("nombre", ""))
        tipo = sanitizar_texto(data.get("tipo", ""))
        edad = data.get("edad")

        try:
            edad = int(edad)
        except ValueError:
            logging.warning("⚠ Edad no válida en `post_mascota()`")  # WARNING
            return jsonify({"error": "Edad debe ser un número entero válido."}), 400

        if not (nombre and 2 <= len(nombre) <= 50):
            return jsonify({"error": "El nombre debe tener entre 2 y 50 caracteres."}), 400
        if tipo not in ["Perro", "Gato", "Ave", "Otro"]:
            return jsonify({"error": "Tipo de mascota no válido."}), 400
        if not (isinstance(edad, int) and edad > 0):
            return jsonify({"error": "Edad debe ser un número entero positivo."}), 400

        # ✅ Generar la mascota con programación defensiva
        nueva_mascota = agregar_mascota(nombre, tipo, edad)
        if nueva_mascota is None:
            raise ValueError("Error: La mascota no se creó correctamente.")

        logging.info(f"✅ Mascota agregada: {nueva_mascota.to_dict()}")  # INFO
        return jsonify(nueva_mascota.to_dict()), 201
    except (AssertionError, ValueError) as ae:
        logging.warning(f"⚠ Validación fallida en `post_mascota()`: {str(ae)}")  # WARNING
        return jsonify({"error": f"Error de validación: {str(ae)}"}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"⚠ Error crítico en `post_mascota()`: {str(e)}")  # ERROR
        return jsonify({"error": f"Error interno al agregar mascota: {str(e)}"}), 500

# ✅ Ruta para eliminar una mascota con control de errores
@mascotas_bp.route("/<int:mascota_id>", methods=["DELETE"])
def eliminar_mascota(mascota_id):
    logging.debug(f"Ejecutando `eliminar_mascota()` con ID {mascota_id}")  # DEBUG
    try:
        mascota = Mascota.query.get(mascota_id)
        if not mascota:
            logging.warning(f"⚠ Intento de eliminación de mascota no existente (ID {mascota_id})")  # WARNING
            return jsonify({"error": "Mascota no encontrada"}), 404

        db.session.delete(mascota)
        db.session.commit()

        logging.info(f"✅ Mascota eliminada: ID {mascota_id}")  # INFO
        return jsonify({"mensaje": f"Mascota con ID {mascota_id} eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"⚠ Error en `eliminar_mascota()`: {str(e)}")  # ERROR
        return jsonify({"error": f"Error al eliminar mascota: {str(e)}"}), 500
=======
from flask import Blueprint, request, jsonify
from services.mascota_service import agregar_mascota, obtener_mascotas

mascotas_bp = Blueprint('mascotas_bp', __name__)

@mascotas_bp.route('/api/test', methods=['GET'])
def test():
    """Ruta de prueba para verificar que el backend está activo."""
    return jsonify({"mensaje": "Funkelin backend activo 🚀"}), 200

@mascotas_bp.route('/api/mascotas', methods=['GET'])
def get_mascotas():
    """Ruta para obtener la lista de todas las mascotas."""
    try:
        mascotas = obtener_mascotas()
        return jsonify([m.to_dict() for m in mascotas]), 200  # Utiliza el método `to_dict` del modelo Mascota
    except Exception as e:
        return jsonify({"error": f"Error al obtener mascotas: {str(e)}"}), 500

@mascotas_bp.route('/api/mascotas', methods=['POST'])
def post_mascota():
    """Ruta para agregar una nueva mascota."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió ningún dato."}), 400
        
        # Validar datos obligatorios
        nombre = data.get("nombre")
        especie = data.get("especie")
        tipo = especie if especie else "Desconocido"  # Tipo predeterminado si no se proporciona especie
        edad = data.get("edad", 1)  # Edad predeterminada si no se proporciona

        if not nombre or not especie:
            return jsonify({"error": "Faltan datos obligatorios: 'nombre' y 'especie' son requeridos."}), 400
        
        # Agregar nueva mascota
        nueva_mascota = agregar_mascota(nombre, tipo, edad)
        return jsonify(nueva_mascota.to_dict()), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar mascota: {str(e)}"}), 500
>>>>>>> f978f38 (Reinstanciación completa del backend:)
