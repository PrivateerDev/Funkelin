import os
import sys
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.models import db
from backend.models.mascota import Mascota

# ✅ Asegurar compatibilidad UTF-8 en stdout
sys.stdout.reconfigure(encoding='utf-8')

# ✅ Configurar logging sin emojis para evitar errores en Windows
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.debug("🔄 Iniciando la configuración de Funkelin API")

# ✅ Diccionario centralizado de errores
ERROR_MESSAGES = {
    "import_fail": "No se pudo importar el Blueprint `mascotas_bp`. Verifica rutas o dependencias.",
    "db_create_fail": "Error al crear las tablas en la base de datos.",
    "unexpected_error": "Error inesperado en la inicialización de la aplicación."
}

# ✅ Instancia de Flask
app = Flask(__name__)

# ✅ Configuración de base de datos
DATABASE_PATH = os.getenv("DATABASE_PATH", "backend/mascotas.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(DATABASE_PATH)}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

logging.info(f"✅ INSTANCIA GLOBAL DE SQLAlchemy CREADA - Base de datos en: {os.path.abspath(DATABASE_PATH)}")

# ✅ Inicializar DB
try:
    db.init_app(app)
    logging.info("✅ BASE DE DATOS INICIALIZADA CON FLASK")
except Exception as e:
    logging.critical(f"⚠ {ERROR_MESSAGES['unexpected_error']} - Detalles: {e}")
    raise RuntimeError(ERROR_MESSAGES["unexpected_error"])

# ✅ Configuración de CORS
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})
logging.info("✅ CORS CONFIGURADO CORRECTAMENTE")

# ✅ Registro de Blueprint
try:
    from backend.routes.mascotas import mascotas_bp
    app.register_blueprint(mascotas_bp)
    logging.info("✅ Blueprint `mascotas_bp` registrado correctamente")
except ImportError as e:
    logging.error(f"⚠ {ERROR_MESSAGES['import_fail']} - Detalles: {e}")

# ✅ Creación de tablas en la base de datos
with app.app_context():
    try:
        db.create_all()
        logging.info("✅ TABLAS CREADAS EXITOSAMENTE")
    except Exception as e:
        logging.error(f"⚠ {ERROR_MESSAGES['db_create_fail']} - Detalles: {e}")

# ✅ Ruta principal
@app.route("/")
def home():
    logging.info("✅ ENDPOINT `/` EJECUTADO CORRECTAMENTE")
    return jsonify({"mensaje": "Bienvenido a Funkelin API Modularizado"}), 200

# ✅ Ruta de depuración
@app.route("/api/debug", methods=["GET"])
def debug():
    """Consulta todos los objetos Mascota registrados en la base de datos."""
    logging.debug("🔄 Ejecutando `debug()` para verificar conexión")
    try:
        with app.app_context():
            mascotas = Mascota.query.all()
            if not mascotas:
                logging.warning("⚠ NO HAY MASCOTAS REGISTRADAS EN LA BASE DE DATOS")
                return jsonify({"mensaje": "No hay mascotas registradas."}), 404

            logging.info(f"✅ SE CONSULTARON {len(mascotas)} MASCOTAS")
            return jsonify([m.to_dict() for m in mascotas]), 200
    except Exception as e:
        logging.error(f"⚠ ERROR EN `debug()`: {str(e)}")
        return jsonify({"error": f"Error al consultar mascotas: {str(e)}"}), 500

# ✅ Ejecución del servidor con control de entorno
if __name__ == "__main__":
    flask_env = os.getenv("FLASK_ENV", "development")
    logging.info(f"✅ INICIANDO FUNKELIN API EN MODO: {flask_env}")
    app.run(debug=(flask_env == "development"))