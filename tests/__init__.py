from flask import Flask
from backend.models import db
from backend.routes.mascotas import mascotas_blueprint

# ✅ Inicialización de la aplicación
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///backend/mascotas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Inicializar la base de datos
db.init_app(app)

# ✅ Registrar blueprints de rutas
app.register_blueprint(mascotas_blueprint, url_prefix="/api/mascotas")

# ✅ Prueba de configuración
@app.route("/")
def home():
    return "Bienvenido a Funkelin API Modularizado 🚀"

# ✅ Importar módulos para evitar referencias circulares
import backend.routes
import backend.models