from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from routes.mascotas import mascotas_bp
from models import db  # Importar db desde models/__init__.py
import os  # Importar os para trabajar con rutas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mascotas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy con Flask
db.init_app(app)

# Imprimir la ubicación de la base de datos
print("Base de datos activa:", os.path.abspath("mascotas.db"))

# Crear tablas en la base de datos
with app.app_context():
    db.create_all()

# Registrar rutas
app.register_blueprint(mascotas_bp)

# Ruta principal
@app.route('/')
def home():
    return "Bienvenido a Funkelin API Modularizado 🚀"

# Ruta de depuración
@app.route('/api/debug', methods=['GET'])
def debug():
    try:
        from models.mascota import Mascota
        mascotas = Mascota.query.all()
        return jsonify([m.to_dict() for m in mascotas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)