import pytest
import json
from backend.app import app  # Importa la aplicación Flask desde backend.app

@pytest.fixture
def client():
    """Fixture para configurar un cliente de pruebas en modo TEST."""
    app.config["TESTING"] = True  # ✅ Establecer modo de prueba
    with app.test_client() as client:
        yield client

def test_home(client):
    """Prueba la ruta principal."""
    response = client.get("/")  # Llama a la ruta principal
    assert response.status_code == 200  # ✅ Verifica código de respuesta
    assert response.get_data(as_text=True) == "Bienvenido a Funkelin API Modularizado 🚀"  # ✅ Forma más clara de extraer texto

def test_api_not_found(client):
    """Prueba una ruta inexistente."""
    response = client.get("/api/inexistente")
    assert response.status_code == 404  # ✅ Verifica que retorna un error 404

def test_debug_endpoint(client):
    """Prueba la ruta de depuración."""
    response = client.get("/api/debug")
    assert response.status_code in [200, 404]  # ✅ Puede retornar mascotas o decir que no hay registros
    data = json.loads(response.data)  # ✅ Extraer JSON para análisis
    assert isinstance(data, dict) or isinstance(data, list)  # ✅ Verificar estructura esperada
