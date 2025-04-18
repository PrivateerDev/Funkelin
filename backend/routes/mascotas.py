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