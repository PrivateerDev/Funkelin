from flask import Blueprint, jsonify
from services.mascota_service import obtener_mascotas

mascotas_bp = Blueprint('mascotas', __name__)

@mascotas_bp.route('/api/mascotas', methods=['GET'])
def get_mascotas():
    mascotas = obtener_mascotas()
    return jsonify([m.to_dict() for m in mascotas])
