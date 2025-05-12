import uuid
import pytest
from fastapi.testclient import TestClient
from app.main.adapter.logger_adapter import Logger
from app.main.main import app
from app.context.user.external.repository.user_repository import UserRepository
from app.main.config.database.db import engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from app.context.user.external.model.user_model import UserModel
from app.main.adapter.hash import get_password_hash
from app.shared.provider.password_provider.bcrypter_adapter import BcryptAdapter
from app.shared.provider.password_provider.password_provider import PasswordProvider

PREFIX = "/api/v1"

# Fixture para TestClient
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture para limpar e preparar o banco antes de cada módulo
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Cria tabelas para teste (assumindo metadata configurada)
    UserModel.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield
    # Limpa dados após testes
    db.query(UserModel).delete()
    db.commit()
    db.close()
    UserModel.metadata.drop_all(bind=engine)

#1. Login bem-sucedido
def test_login_successful(client):
    # Prepara usuário no banco
    db = SessionLocal()
    password = "secret123"
    
    cryptAdapter = BcryptAdapter()
    passwordProvider = PasswordProvider(Logger(), cryptAdapter)
    result = passwordProvider.hash(password)
    
    user = UserModel(
        name="Teste",
        email="teste@example.com",
        document="12345678901",
        password=result.get_value().get("hash"),
        salt=result.get_value().get("salt"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post(
       PREFIX + "/user/login",
        json={"document": "12345678901", "password": "secret123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "token" in body and "refresh" in body
    db.close()

# 2. Usuário não encontrado
def test_login_user_not_found(client):
    response = client.post(
        PREFIX + "/user/login",
        json={"document": "00000000000", "password": "doesntmatter"}
    )
    assert response.status_code == 404
    assert response.json()["error"] == "User not found"

# 3. Senha incorreta
def test_login_wrong_password(client):
    # Prepara usuário
    db = SessionLocal()
    user = UserModel(
        name="Teste2",
        email="teste2@example.com",
        document="10987654321",
        password_hash=get_password_hash("correctpwd")
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post(
        PREFIX + "/user/login",
        json={"document": "10987654321", "password": "wrongpwd"}
    )
    assert response.status_code == 404
    db.close()

# 4. Payload incompleto
@pytest.mark.parametrize(
    "payload",
    [
        {"password": "pwdonly"},
        {"document": "12345678901"},
        {}
    ]
)
def test_login_incomplete_payload(client, payload):
    response = client.post( PREFIX + "/user/login", json=payload)
    assert response.status_code == 404

# 5. Payload inválido (tipos errados)
def test_login_invalid_payload_types(client):
    response = client.post(
        PREFIX + "/user/login",
        json={"document": 123, "password": True}
    )
    assert response.status_code == 404

# 6. Header Authorization ignorado na login route
def test_login_ignores_auth_header(client):
    # Mesmo comportamento de sucesso com header inválido
    response = client.post(
         PREFIX + "/user/login",
        headers={"Authorization": "Bearer invalidtoken"},
        json={"document": "12345678901", "password": "secret123"}
    )
    # Pode retornar 401 se user não existir, mas não 400 por header
    assert response.status_code == 404
