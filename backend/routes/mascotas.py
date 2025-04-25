from flask import Blueprint, request, jsonify
from flask_cors import CORS  # ✅ Importar flask-cors para permitir solicitudes desde el frontend
from backend.models import db  # ✅ Importar db desde models para evitar conflictos
from backend.models.mascota import Mascota
from backend.services.mascota_service import agregar_mascota, obtener_mascotas

# ✅ Definir el blueprint con un prefijo más estructurado
mascotas_bp = Blueprint("mascotas", __name__, url_prefix="/api/mascotas")

# ✅ Habilitar CORS en las rutas de mascotas
CORS(mascotas_bp, resources={r"/api/*": {"origins": "*"}})

# ✅ Ruta de prueba
@mascotas_bp.route("/test", methods=["GET"])
def test():
    """Ruta de prueba para verificar que el backend está activo."""
    return jsonify({"mensaje": "Funkelin backend activo 🚀"}), 200

# ✅ Ruta para obtener la lista de todas las mascotas
@mascotas_bp.route("/", methods=["GET"])
def get_mascotas():
    """Retorna la lista de mascotas registradas."""
    try:
        mascotas = obtener_mascotas()  # ✅ Usa el servicio en lugar de consulta directa
        return jsonify(mascotas), 200
    except Exception as e:
        db.session.rollback()  # ✅ Asegurar que no queden transacciones abiertas
        return jsonify({"error": f"Error al obtener mascotas: {str(e)}"}), 500

# ✅ Ruta para agregar una nueva mascota
@mascotas_bp.route("/", methods=["POST"])
def post_mascota():
    """Agrega una nueva mascota al sistema."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió ningún dato."}), 400

        nombre = data.get("nombre", "").strip()
        especie = data.get("especie", "").strip()
        tipo = especie if especie else "Desconocido"
        edad = data.get("edad", 1)

        if not nombre or not especie or edad <= 0:
            return jsonify({"error": "Faltan datos obligatorios: 'nombre', 'especie' y 'edad' deben ser válidos."}), 400

        nueva_mascota = agregar_mascota(nombre, tipo, edad)  # ✅ Usa el servicio en lugar de consulta directa
        return jsonify(nueva_mascota.to_dict()), 201
    except ValueError as ve:
        db.session.rollback()  # ✅ Evitar bloqueos en la base de datos
        return jsonify({"error": f"Error de validación: {str(ve)}"}), 400
    except Exception as e:
        db.session.rollback()  # ✅ Asegurar que no quede una transacción en estado inconsistente
        return jsonify({"error": f"Error interno al agregar mascota: {str(e)}"}), 500
