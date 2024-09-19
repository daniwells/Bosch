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

def test_list_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/contas-pagar-receber', json={'id': 1, 'description': 'Rent', 'value': 1000.5, 'type': 'PAY'})
    client.post('/contas-pagar-receber', json={'id': 2, 'description': 'Bought', 'value': 5000.0, 'type': 'RECEIVE'})
    response = client.get("/contas-pagar-receber")
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'description': 'Rent', 'value': 1000.5, 'type': 'PAY'}, 
        {'id': 2, 'description': 'Bought', 'value': 5000.0, 'type': 'RECEIVE'}
    ]


def test_get_conta_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post('/contas-pagar-receber', json={
        'id': 1, 
        'description': 'Rent', 
        'value': 1000.5, 
        'type': 'PAY'
    })

    id_conta_pagar_receber = response_post.json()['id']

    response = client.get(f"/contas-pagar-receber/{id_conta_pagar_receber}")

    assert response.status_code == 200
    assert response.json()['value'] == 1000.5
    assert response.json()['type'] == "PAY"
    assert response.json()['description'] == "Rent"


def test_error_get_conta_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post('/contas-pagar-receber', json={
        'id': 1, 
        'description': 'Rent', 
        'value': 1000.5, 
        'type': 'PAY'
    })

    response = client.get(f"/contas-pagar-receber/1000000")

    assert response.status_code == 404


def test_create_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_account = {
        "description": "curse of python",
        "value": 333,
        "type": "PAY"
    }

    new_account_copy = new_account.copy()

    new_account_copy["id"] = 1

    response = client.post("/contas-pagar-receber/", json=new_account_copy)
    assert response.status_code == 201
    assert response.json() == new_account_copy


def test_update_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/contas-pagar-receber/", json={
        "description": "curse of python",
        "value": 333,
        "type": "PAY"
    })

    id_conta_pagar_receber = response_post.json()['id']

    response_put = client.put(f"/contas-pagar-receber/{id_conta_pagar_receber}", json={
        "description": "curse of python",
        "value": 111,
        "type": "PAY"
    })

    assert response_post.status_code == 201
    assert response_put.status_code == 200
    assert response_put.json()['value'] == 111


def test_error_update_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/contas-pagar-receber/", json={
        "description": "curse of python",
        "value": 333,
        "type": "PAY"
    })

    response_put = client.put(f"/contas-pagar-receber/100000", json={
        "description": "curse of python",
        "value": 111,
        "type": "PAY"
    })

    assert response_post.status_code == 201
    assert response_put.status_code == 404


def test_remove_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/contas-pagar-receber/", json={
        "description": "curse of python",
        "value": 333,
        "type": "PAY"
    })

    id_conta_pagar_receber = response_post.json()['id']

    response_delete = client.delete(f"/contas-pagar-receber/{id_conta_pagar_receber}")

    assert response_post.status_code == 201
    assert response_delete.status_code == 204


def test_error_remove_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/contas-pagar-receber/", json={
        "description": "curse of python",
        "value": 333,
        "type": "PAY"
    })

    response_delete = client.delete(f"/contas-pagar-receber/1000")

    assert response_post.status_code == 201
    assert response_delete.status_code == 404


def test_return_error_when_exceded_decription():
    response = client.post('/contas-pagar-receber', json={
        "description":"010100101khkjhkjhkjhkjhkjhkjhkjhkjhkjkjhkjhkjhkjhkjh01010100",
        "value":333,
        "type":"PAY"
    })

    assert response.status_code == 422


def teste_return_error_when_description_less_than_necessary():
    response = client.post('/contas-pagar-receber', json={
        "description":"01",
        "value":3,
        "type":"PAY"
    })

    assert response.status_code == 422


def test_return_error_when_value_0_or_less():

    response = client.post('/contas-pagar-receber', json={
        "description":"010100101khkjhkjhkjhkjhkjhkjhkjhkjhkjkjhkjhkjhkjhkjh01010100",
        "value":0,
        "type":"PAY"
    })

    assert response.status_code == 422

    response = client.post('/contas-pagar-receber', json={
        "description":"010100101khkjhkjhkjhkjhkjhkjhkjhkjhkjkjhkjhkjhkjhkjh01010100",
        "value":-1,
        "type":"PAY"
    })

    assert response.status_code == 422

def test_return_invalide_type():
    response = client.post('/contas-pagar-receber', json={
        "description":"asdasdasddsa",
        "value":0,
        "type":"KKKKK"
    })

    assert response.status_code == 422