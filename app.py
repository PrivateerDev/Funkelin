from flask import Flask
from routes.mascotas import mascotas_bp
from services.mascota_service import agregar_mascota  # 👈 Importas la función
from flask_cors import CORS  # 👈 Importación para habilitar CORS

app = Flask(__name__)
CORS(app)  # 👈 Habilita CORS para todas las rutas
app.register_blueprint(mascotas_bp)

@app.route('/')
def home():
    return "Bienvenido a Funkelin API Modularizado"

# 👇 Esta parte la agregas para probar que se guarden mascotas
@app.route('/api/agregar_demo')
def agregar_demo():
    agregar_mascota("Luna", "Gato")
    return "Mascota agregada"

if __name__ == '__main__':
    app.run(debug=True)