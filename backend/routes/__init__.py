# routes/init.py
# Este archivo marca `routes` como un módulo y permite la importación de rutas.

from backend.routes.mascotas import mascotas_bp

blueprints = [mascotas_bp]  # ✅ Agrega otros Blueprints si es necesario
