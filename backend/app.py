<<<<<<< HEAD
import os
import logging
import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.models import db
from backend.models.mascota import Mascota

# ✅ Configurar logging con soporte UTF-8 y control de niveles
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_app.log", encoding="utf-8"),  # ✅ Asegurar codificación en archivos
        logging.StreamHandler(sys.stdout)  # ✅ Evitar errores de codificación en consola
    ]
)

# ✅ Configurar `StreamHandler` con control de salida en consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # ✅ Limitar la consola solo a INFO y superiores
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# ✅ Agregar el manejador al `root logger`
logging.getLogger().addHandler(console_handler)

logging.debug("🛠️ Iniciando configuración principal de Funkelin")  # DEBUG

# ✅ Configuración segura de la aplicación Flask
app = Flask(__name__)

# ✅ Obtener la URI de la base de datos desde variables de entorno
DATABASE_PATH = os.getenv("DATABASE_PATH", "backend/mascotas.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(DATABASE_PATH)}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

logging.info(f"✅ Base de datos configurada en: {os.path.abspath(DATABASE_PATH)}")  # INFO

# ✅ Inicializar la base de datos con la aplicación Flask
db.init_app(app)
logging.info("✅ Base de datos inicializada con Flask")  # INFO

# ✅ Habilitar CORS con control refinado de accesos
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})
logging.info("✅ CORS configurado correctamente")  # INFO

# ✅ Registrar rutas después de inicializar `app` y `db`
try:
    from backend.routes.mascotas import mascotas_bp
    app.register_blueprint(mascotas_bp)
    logging.info("✅ Blueprint `mascotas_bp` registrado exitosamente")  # INFO
except ImportError as e:
    logging.error(f"⚠️ Error al registrar `mascotas_bp`: {e}")  # ERROR

# ✅ Crear tablas dentro del contexto de Flask con manejo seguro de errores
logging.debug("🛠️ Creando tablas en la base de datos")  # DEBUG
with app.app_context():
    try:
        db.create_all()
        logging.info("✅ Tablas creadas exitosamente")  # INFO
    except Exception as e:
        logging.error(f"⚠️ Error al crear tablas en la base de datos: {e}")  # ERROR

# ✅ Ruta principal
@app.route("/")
def home():
    logging.info("✅ Endpoint `/` ejecutado correctamente")  # INFO
    return jsonify({"mensaje": "Bienvenido a Funkelin API Modularizado 🚀"}), 200

# ✅ Ruta de depuración con validación de conexión
@app.route("/api/debug", methods=["GET"])
def debug():
    """Consulta todos los objetos Mascota registrados en la base de datos con manejo seguro."""
    logging.debug("🔎 Ejecutando `debug()` para verificar conexión con la base de datos")  # DEBUG
    try:
        with app.app_context():
            if not db.session.is_active:
                raise RuntimeError("⚠️ La conexión con la base de datos no está activa.")

            mascotas = Mascota.query.all()
            if not mascotas:
                logging.warning("⚠️ No hay mascotas registradas en la base de datos")  # WARNING
                return jsonify({"mensaje": "No hay mascotas registradas."}), 404

            logging.info(f"✅ Se consultaron {len(mascotas)} mascotas")  # INFO
            return jsonify([m.to_dict() for m in mascotas]), 200
    except RuntimeError as re:
        logging.error(f"⚠️ Error de conexión: {str(re)}")  # ERROR
        return jsonify({"error": f"Error de conexión a la base de datos: {str(re)}"}), 500
    except Exception as e:
        logging.error(f"⚠️ Error crítico en `debug()`: {str(e)}")  # ERROR
        return jsonify({"error": f"Error al consultar mascotas: {str(e)}"}), 500

# ✅ Ejecutar la aplicación en modo seguro con control de entorno
if __name__ == "__main__":
    flask_env = os.getenv("FLASK_ENV", "development")
    logging.info(f"🚀 Iniciando Funkelin API en modo: {flask_env}")  # INFO
    app.run(debug=(flask_env == "development"))
=======
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
>>>>>>> f978f38 (Reinstanciación completa del backend:)
