import pytest
import os
from app import app, init_db, DB_FILE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    if not os.path.exists(DB_FILE):
        init_db()
    with app.test_client() as client:
        yield client

def test_smoke_home(client):
    """Ciclo 1: Smoke Test - Carga de Home"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Bienvenido a la Tienda de Pruebas" in rv.data

def test_cp_001_login_sql(client):
    """CP-001: Login con SQL (Aprueba) - Manejo de error genérico en intento de inyección"""
    rv = client.post('/login', json={'username': "admin' OR 1=1 --", 'password': '123'})
    assert rv.status_code == 400
    assert b"Error de inicio de sesi" in rv.data

def test_cp_002_registro_usuario(client):
    """CP-002: Registro de usuario (Falla) - Falla intencional del sistema"""
    with pytest.raises(Exception, match="Error interno"):
        client.post('/register', json={'username': 'nuevo', 'password': '123'})

@pytest.mark.skip(reason="Bloqueado por fallo en registro (CP-002)")
def test_cp_003_compra_producto(client):
    """CP-003: Compra de producto (Bloqueado)"""
    client.post('/buy', json={'product_id': 1})
