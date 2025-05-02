"""Módulo de inicialización para rutas en Funkelin."""

from flask import Blueprint

# ✅ Importa los Blueprints de cada módulo de rutas
from backend.routes.mascotas import mascotas_bp

# ✅ Lista de Blueprints registrados en el sistema
blueprints = [mascotas_bp]

def register_blueprints(app):
    """Registra todos los Blueprints en la aplicación Flask."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)