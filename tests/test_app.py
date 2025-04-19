import pytest
from backend.app import app  # Importa la aplicación Flask desde backend.app

@pytest.fixture
def client():
    """Fixture para configurar un cliente de pruebas."""
    with app.test_client() as client:
        yield client

def test_home(client):
    """Prueba la ruta principal."""
    response = client.get("/")  # Llama a la ruta principal
    assert response.status_code == 200  # Verifica que el código de estado sea 200
    assert response.data.decode("utf-8") == "Bienvenido a Funkelin API Modularizado 🚀"  # Verifica el mensaje esperado
