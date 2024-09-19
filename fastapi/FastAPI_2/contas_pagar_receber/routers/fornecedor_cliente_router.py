from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_pagar_receber.models.fornecedor_cliente_model import FornecedorCliente
from shared.dependencies import get_db
from shared.exceptions import NotFound
import copy

router = APIRouter(prefix="/fornecedor_cliente")

class FornecedorClienteResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class FornecedorClienteRequest(BaseModel):
    name: str = Field(min_length=3, max_length=255)


@router.get("", response_model=List[FornecedorClienteResponse])
def list_fornecedor_cliente(db: Session = Depends(get_db)) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).all()


@router.get("/{id_fornecedor_cliente}", response_model=FornecedorClienteResponse)
def get_fornecedor_cliente_by_id(id_fornecedor_cliente: int, 
                                db: Session = Depends(get_db)) -> List[FornecedorClienteResponse]:

    return search_fornecedor_cliente_by_id(id_fornecedor_cliente, db)


@router.post("", response_model=FornecedorClienteResponse, status_code=201)
def post_fornecedor_cliente(fornecedor_cliente_request: FornecedorClienteRequest, 
                            db: Session = Depends(get_db)) -> FornecedorClienteResponse:

    fornecedor_cliente = FornecedorCliente(
        **fornecedor_cliente_request.dict()
    )

    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)

    return fornecedor_cliente


@router.put("/{id_fornecedor_cliente}", response_model=FornecedorClienteResponse, status_code=200)
def put_fornecedor_cliente(id_fornecedor_cliente: int, 
                            fornecedor_cliente_request: FornecedorClienteRequest, 
                            db: Session = Depends(get_db)) -> FornecedorClienteResponse: 

    fornecedor_cliente = search_fornecedor_cliente_by_id(id_fornecedor_cliente, db)

    # for key, value in fornecedor_cliente_request.dict().items():
    #     setattr(fornecedor_cliente, key, value)

    fornecedor_cliente.name = fornecedor_cliente_request.name

    db.commit()
    db.refresh(fornecedor_cliente)
    return fornecedor_cliente


@router.delete("/{id_fornecedor_cliente}", status_code=204)
def delete_fornecedor_cliente(id_fornecedor_cliente: int, 
                            db: Session = Depends(get_db)) -> None:

    fornecedor_cliente = search_fornecedor_cliente_by_id(id_fornecedor_cliente, db)

    db.delete(fornecedor_cliente)
    db.commit()


def search_fornecedor_cliente_by_id(id_fornecedor_cliente: int, db: Session) -> None:
    fornecedor_cliente = db.query(FornecedorCliente).get(id_fornecedor_cliente)

    if fornecedor_cliente is None:
        raise NotFound("Fornecedor Cliente")

    return fornecedor_cliente