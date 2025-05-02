import pytest
import json
from backend.app import app  # ✅ Importa la aplicación Flask

@pytest.fixture
def client():
    """Fixture para configurar un cliente de pruebas en modo TEST."""
    app.config["TESTING"] = True  # ✅ Establece modo de prueba
    app.config["DEBUG"] = False   # ✅ Desactiva mensajes de depuración excesivos
    with app.test_client() as client:
        yield client

def test_home(client):
    """Prueba la ruta principal."""
    response = client.get("/")  # ✅ Llama a la ruta principal
    assert response.status_code == 200, "⚠ Error: Código de respuesta inesperado"
    assert "Bienvenido a Funkelin API Modularizado" in response.get_data(as_text=True), "⚠ Error en mensaje de bienvenida"

def test_api_not_found(client):
    """Prueba una ruta inexistente."""
    response = client.get("/api/inexistente")
    assert response.status_code == 404, "⚠ Error: La API no está manejando correctamente rutas inexistentes"

def test_api_mascotas(client):
    """Prueba la ruta de obtención de mascotas."""
    response = client.get("/api/mascotas/")
    assert response.status_code == 200, "⚠ Error: La ruta de mascotas no responde correctamente"
    data = json.loads(response.data)  
    assert isinstance(data, list), "⚠ Error: La API debería retornar una lista"
    assert all(isinstance(mascota, dict) for mascota in data), "⚠ Error: Cada mascota debe ser un diccionario válido"

def test_agregar_mascota(client):
    """Prueba la creación de una mascota."""
    nueva_mascota = {"nombre": "Rocky", "tipo": "Perro", "edad": 2}
    response = client.post("/api/mascotas/", json=nueva_mascota)
    assert response.status_code == 201, "⚠ Error: No se agregó correctamente la mascota"

def test_eliminar_mascota(client):
    """Prueba la eliminación de una mascota."""
    response = client.delete("/api/mascotas/1")  # Intentar eliminar ID 1
    assert response.status_code in [200, 404], "⚠ Error: La eliminación no está funcionando correctamente"