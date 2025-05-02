import re
from flask import Blueprint, request, jsonify
from flask_cors import CORS  # ✅ Permitir solicitudes del frontend
from backend.models import db  # ✅ Evitar conflictos en importaciones
from backend.models.mascota import Mascota
from backend.services.mascota_service import agregar_mascota, obtener_mascotas

# ✅ Definir el blueprint con un prefijo más estructurado
mascotas_bp = Blueprint("mascotas", __name__, url_prefix="/api/mascotas")

# ✅ Habilitar CORS en las rutas de mascotas
CORS(mascotas_bp, resources={r"/api/*": {"origins": "*"}})  # ✅ Evita restricciones innecesarias

# ✅ Ruta de prueba
@mascotas_bp.route("/test", methods=["GET"])
def test():
    """Ruta de prueba para verificar que el backend está activo."""
    return jsonify({"mensaje": "Funkelin backend activo 🚀"}), 200

# ✅ Función para sanitizar texto de entrada
def sanitizar_texto(texto):
    """Elimina caracteres peligrosos y espacios extra."""
    return re.sub(r'[<>"\'&]', '', texto).strip()

# ✅ Ruta para obtener la lista de todas las mascotas
@mascotas_bp.route("/", methods=["GET"])
def get_mascotas():
    """Retorna la lista de mascotas registradas con manejo de errores."""
    try:
        mascotas = obtener_mascotas()
        assert isinstance(mascotas, list), "Error: La respuesta de obtener_mascotas debe ser una lista."

        return jsonify(mascotas), 200  # ✅ Ahora las mascotas se devuelven correctamente
    except AssertionError as ae:
        return jsonify({"error": f"Error interno de validación: {str(ae)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al obtener mascotas: {str(e)}"}), 500

# ✅ Ruta para agregar una nueva mascota con sanitización y validaciones defensivas
@mascotas_bp.route("/", methods=["POST"])
def post_mascota():
    """Agrega una nueva mascota al sistema con validaciones estrictas."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió ningún dato."}), 400

        # ✅ Sanitización y validaciones de entrada
        nombre = sanitizar_texto(data.get("nombre", ""))
        especie = sanitizar_texto(data.get("especie", "")).strip()
        edad = data.get("edad")

        # ✅ Conversión segura de edad a entero
        try:
            edad = int(edad)
        except ValueError:
            return jsonify({"error": "Edad debe ser un número entero válido."}), 400

        assert isinstance(nombre, str) and 2 <= len(nombre) <= 50, "El nombre debe tener entre 2 y 50 caracteres."
        assert isinstance(especie, str) and especie in ["Perro", "Gato", "Ave", "Otro"], "Especie no válida."
        assert isinstance(edad, int) and edad > 0, "Edad debe ser un número entero positivo."

        # ✅ Generar la mascota con programación defensiva
        nueva_mascota = agregar_mascota(nombre, especie, edad)

        # ✅ Postcondición: verificar que se creó correctamente
        assert nueva_mascota is not None, "Error: La mascota no se creó correctamente."

        return jsonify(nueva_mascota.to_dict()), 201  # ✅ Ahora convertimos el objeto a JSON correctamente
    except AssertionError as ae:
        return jsonify({"error": f"Error de validación: {str(ae)}"}), 400
    except ValueError as ve:
        db.session.rollback()
        return jsonify({"error": f"Error de validación: {str(ve)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error interno al agregar mascota: {str(e)}"}), 500

# ✅ Ruta para eliminar una mascota por su ID con manejo de errores
@mascotas_bp.route("/<int:mascota_id>", methods=["DELETE"])
def eliminar_mascota(mascota_id):
    """Elimina una mascota por su ID con manejo de errores."""
    try:
        mascota = Mascota.query.get(mascota_id)
        if not mascota:
            return jsonify({"error": "Mascota no encontrada"}), 404

        db.session.delete(mascota)
        db.session.commit()

        return jsonify({"mensaje": f"Mascota con ID {mascota_id} eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar mascota: {str(e)}"}), 500
