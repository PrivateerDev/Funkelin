import logging
import os
from flask import Flask
from backend.models import db

# ✅ Configurar logging para auditoría de inicialización de la base de datos
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/logs/funkelin_db_init.log"),
        logging.StreamHandler()
    ]
)

logging.debug("Iniciando configuración de la base de datos en `init_db.py`")  # DEBUG

# ✅ Configuración de la aplicación Flask
app = Flask(__name__)
DATABASE_PATH = os.path.abspath("backend/mascotas.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

logging.info(f"✅ Base de datos configurada en: {DATABASE_PATH}")  # INFO

# ✅ Inicializar la base de datos
db.init_app(app)
logging.info("✅ Base de datos vinculada correctamente con la aplicación Flask")  # INFO

# ✅ Crear la base de datos dentro del contexto de Flask con manejo seguro de errores
logging.debug("Creando tablas en la base de datos")  # DEBUG
with app.app_context():
    try:
        db.create_all()
        logging.info("✅ Tablas creadas exitosamente")  # INFO
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        logging.error(f"⚠ Error al crear tablas en la base de datos: {e}")  # ERROR

logging.debug("Finalizando `init_db.py`")  # DEBUG