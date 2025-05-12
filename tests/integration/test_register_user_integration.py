# tests/integration/test_register_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main.main import app
from app.main.config.database.db import engine, SessionLocal
from app.context.user.external.model.user_model import UserModel
from app.main.adapter.hash import get_password_hash

PREFIX = "/api/v1"

# Fixture para TestClient
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture para limpar e preparar o banco antes de cada módulo
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Cria tabelas para teste
    UserModel.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield
    # Limpa dados após testes
    db.query(UserModel).delete()
    db.commit()
    db.close()
    UserModel.metadata.drop_all(bind=engine)

# 1. Registro válido
def test_register_successful(client):
    payload = {
        "name": "Teste",
        "email": "teste@example.com",
        "document": "12345678901",
        "password": "secret123"
    }
    response = client.post(PREFIX + "/user/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    # Verifica campos retornados
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["document"] == payload["document"]
    assert "created_at" in data

# 2. E-mail inválido
def test_register_invalid_email(client):
    payload = {
        "name": "Teste",
        "email": "invalid-email",
        "document": "12345678901",
        "password": "secret123"
    }
    response = client.post(PREFIX + "/user/register", json=payload)
    assert response.status_code == 400

# 3. Documento tamanho incorreto
@pytest.mark.parametrize("doc", ["123", "123456789012"])
def test_register_invalid_document_length(client, doc):
    payload = {
        "name": "Teste",
        "email": "teste2@example.com",
        "document": doc,
        "password": "secret123"
    }
    response = client.post(PREFIX + "/user/register", json=payload)
    assert response.status_code == 400

# 4. Senha muito curta
def test_register_short_password(client):
    payload = {
        "name": "Teste",
        "email": "teste3@example.com",
        "document": "12345678901",
        "password": "123"
    }
    response = client.post(PREFIX + "/user/register", json=payload)
    assert response.status_code == 400

# 5. Campo obrigatório ausente
@pytest.mark.parametrize("payload", [
    {"email": "a@b.com", "document": "12345678901", "password": "secret123"},
    {"name": "Teste", "document": "12345678901", "password": "secret123"},
    {"name": "Teste", "email": "a@b.com", "password": "secret123"},
    {"name": "Teste", "email": "a@b.com", "document": "12345678901"}
])
def test_register_missing_field(client, payload):
    response = client.post(PREFIX + "/user/register", json=payload)
    assert response.status_code == 400

# 6. E-mail já cadastrado
def test_register_duplicate_email(client):
    db = SessionLocal()
    # Cria usuário existente
    pwd = get_password_hash("secret123")
    user = UserModel(
        name="Existente",
        email="dup@example.com",
        document="99999999999",
        password_hash=pwd
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    payload = {
        "name": "Teste",
        "email": "dup@example.com",
        "document": "12345678901",
        "password": "secret123"
    }
    response = client.post(PREFIX + "/user/register", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "E-mail já cadastrado"

# 7. Documento já cadastrado
def test_register_duplicate_document(client):
    db = SessionLocal()
    pwd = get_password_hash("secret123")
    user = UserModel(
        name="Existente2",
        email="unique@example.com",
        document="88888888888",
        password_hash=pwd
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    payload = {
        "name": "Teste",
        "email": "new@example.com",
        "document": "88888888888",
        "password": "secret123"
    }
    response = client.post(PREFIX + "/user/register", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "Documento já cadastrado"

# 8. Campos extras no payload
def test_register_ignore_extra_fields(client):
    payload = {
        "name": "Teste",
        "email": "teste4@example.com",
        "document": "12345678901",
        "password": "secret123",
        "foo": "bar"
    }
    response = client.post(PREFIX + "/user/register", json=payload)
    # extras são ignorados por default, então sucesso 201
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "foo" not in data
