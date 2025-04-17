from services.mascota_service import agregar_mascota

@app.route('/api/agregar_demo')
def demo():
    agregar_mascota("Luna", "Gato")
    return "Mascota agregada"
