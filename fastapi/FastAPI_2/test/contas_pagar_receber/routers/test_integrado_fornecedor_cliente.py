from fastapi.testclient import TestClient
from main import app
import copy
from shared.dependencies import get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from shared.database import Base

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_list_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/fornecedor_cliente", json={"id": 1, "name": "test"})
    response = client.get("/contas-pagar-receber")
    assert response.status_code == 200


def test_get_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor_cliente", json={
        "id": 1,
        "name": "test",
    })

    id_fornecedor_cliente = response_post.json()["id"]

    response_get = client.get(f"/fornecedor_cliente/{id_fornecedor_cliente}")

    assert response_get.status_code == 200
    assert response_get.json()["name"] == "test"


def test_error_get_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.get(f"/fornecedor_cliente/1000000")

    assert response.status_code == 404


def test_create_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_account = {
        "id": 1,
        "name": "test",
    }

    new_account_copy = new_account.copy()

    new_account_copy["id"] = 1

    response = client.post("/fornecedor_cliente/", json=new_account_copy)
    assert response.status_code == 201
    assert response.json() == new_account_copy


def test_update_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor_cliente/", json={
        "name": 'test'
    })

    id_fornecedor_cliente = response_post.json()["id"]

    response_put = client.put(f"/fornecedor_cliente/{id_fornecedor_cliente}", json={
        "name": "AAAAAAAAAAAAAAAAAAA"
    })

    assert response_post.status_code == 201
    assert response_put.status_code == 200
    assert response_put.json()["name"] == "AAAAAAAAAAAAAAAAAAA"


def test_error_update_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor_cliente/", json={
        "name": 'test'
    })

    response_put = client.put(f"/fornecedor_cliente/1000000000", json={
        "name": "AAAAAAAAAAAAAAAAAAA"
    })

    assert response_post.status_code == 201
    assert response_put.status_code == 404


def test_remove_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor_cliente/", json={
        "name": "test"
    })

    id_fornecedor_cliente = response_post.json()["id"]

    response_delete = client.delete(f"/fornecedor_cliente/{id_fornecedor_cliente}")

    assert response_post.status_code == 201
    assert response_delete.status_code == 204


def test_error_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor_cliente/", json={
        "name": "teste",
    })

    response_delete = client.delete(f"/fornecedor_cliente/1000")

    assert response_post.status_code == 201
    assert response_delete.status_code == 404


def test_return_invalide_name():
    response = client.post("/fornecedor_cliente", json={
        "name":22222,
    })

    assert response.status_code == 422