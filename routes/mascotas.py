from flask import Blueprint, jsonify, request
from services.mascota_service import obtener_mascotas, agregar_mascota

mascotas_bp = Blueprint('mascotas', __name__)

# Endpoint POST para agregar mascotas
@mascotas_bp.route('/api/mascotas', methods=['POST'])
def post_mascota():
    data = request.get_json()

    # Validar que los datos están presentes
    nombre = data.get("nombre")
    especie = data.get("especie")

    if not nombre or not especie:
        return jsonify({"error": "Faltan datos: 'nombre' y 'especie' son obligatorios"}), 400

    # Validar que el nombre tenga al menos 2 caracteres
    if len(nombre) < 2:
        return jsonify({"error": "El nombre debe tener al menos 2 caracteres"}), 400

    # Validar que la especie sea "Perro" o "Gato" (puedes agregar más opciones si lo deseas)
    if especie.lower() not in ["perro", "gato"]:
        return jsonify({"error": "La especie debe ser 'Perro' o 'Gato'"}), 400

    # Si todo está bien, agregar la nueva mascota
    nueva = agregar_mascota(nombre, especie)
    return jsonify(nueva.to_dict()), 201

# Endpoint GET para obtener todas las mascotas
@mascotas_bp.route('/api/mascotas', methods=['GET'])
def get_mascotas():
    mascotas = obtener_mascotas()  # Función que obtiene todas las mascotas registradas
    return jsonify([m.to_dict() for m in mascotas])