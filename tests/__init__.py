# test/init.py
# Este archivo marca `test` como un módulo y permite la importación de pruebas.

import pytest
from backend.app import app

@pytest.fixture
def client():
    """Fixture global para configurar un cliente de pruebas en Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
