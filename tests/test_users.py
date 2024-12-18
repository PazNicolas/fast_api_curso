import pytest
from fastapi.testclient import TestClient
from main import app, User
from config.database import Session, engine, Base
from models.user import User as UserModel
import bcrypt

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user(setup_database):
    response = client.post("/users", json={"email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 201
    assert response.json() == {"message": "Usuario creado"}

def test_get_users(setup_database):
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_user(setup_database):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_update_user(setup_database):
    response = client.put("/users/1", json={"email": "updateduser@example.com", "password": "newpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "El usuario ha sido actualizado"}

def test_delete_user(setup_database):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "El usuario ha sido eliminado"}

def test_jwt_authentication():
    response = client.post("/login", json={"email": "admin@gmail.com", "password": "admin"})
    assert response.status_code == 200
    token = response.json()

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/movies", headers=headers)
    assert response.status_code == 200
