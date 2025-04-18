from flask import Blueprint, jsonify, request
from services.mascota_service import obtener_mascotas, agregar_mascota

mascotas_bp = Blueprint('mascotas', __name__)

@mascotas_bp.route('/api/mascotas', methods=['GET'])
def get_mascotas():
    """Ruta para obtener la lista de todas las mascotas."""
    mascotas = obtener_mascotas()
    return jsonify([vars(m) for m in mascotas]), 200  # Convertir las mascotas a JSON con `vars`

@mascotas_bp.route('/api/mascotas', methods=['POST'])
def post_mascota():
    """Ruta para agregar una nueva mascota."""
    data = request.get_json()

    # Validar y obtener los datos
    nombre = data.get("nombre")
    especie = data.get("especie")
    tipo = especie if especie else "Desconocido"  # Usar 'especie' como 'tipo', o valor por defecto
    edad = data.get("edad", 1)  # Asignar edad predeterminada si no se pasa en la solicitud

    # Validar datos
    if not nombre or not especie:
        return jsonify({"error": "Faltan datos obligatorios: 'nombre' y 'especie' son necesarios"}), 400
    if len(nombre) < 2:
        return jsonify({"error": "El nombre debe tener al menos 2 caracteres"}), 400
    if especie.lower() not in ["perro", "gato"]:
        return jsonify({"error": "La especie debe ser 'Perro' o 'Gato'"}), 400

    # Crear nueva mascota
    nueva_mascota = agregar_mascota(nombre, tipo, edad)  # Pasar datos correctamente
    return jsonify(vars(nueva_mascota)), 201  # Convertir la nueva mascota a JSON