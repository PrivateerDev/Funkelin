from flask import Blueprint, request, jsonify
from backend.services.mascota_service import agregar_mascota, obtener_mascotas  # Ajustar la importación

# Definir el blueprint
mascotas_bp = Blueprint("mascotas", __name__, url_prefix="/api/mascotas")

# Ruta de prueba
@mascotas_bp.route("/test", methods=["GET"])
def test():
    """Ruta de prueba para verificar que el backend está activo."""
    return jsonify({"mensaje": "Funkelin backend activo 🚀"}), 200


# Ruta para obtener la lista de todas las mascotas
@mascotas_bp.route("/", methods=["GET"])
def get_mascotas():
    """Devuelve la lista de todas las mascotas registradas."""
    try:
        mascotas = obtener_mascotas()
        return jsonify([m.to_dict() for m in mascotas]), 200  # Convierte mascotas a dict
    except Exception as e:
        return jsonify({"error": f"Error al obtener mascotas: {str(e)}"}), 500


# Ruta para agregar una nueva mascota
@mascotas_bp.route("/", methods=["POST"])
def post_mascota():
    """Agrega una nueva mascota al sistema."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió ningún dato."}), 400

        # Validar datos obligatorios
        nombre = data.get("nombre")
        especie = data.get("especie")
        tipo = especie if especie else "Desconocido"  # Tipo predeterminado
        edad = data.get("edad", 1)  # Edad predeterminada

        if not nombre or not especie:
            return jsonify({"error": "Faltan datos obligatorios: 'nombre' y 'especie' son requeridos."}), 400

        # Agregar nueva mascota
        nueva_mascota = agregar_mascota(nombre, tipo, edad)
        return jsonify(nueva_mascota.to_dict()), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar mascota: {str(e)}"}), 500
