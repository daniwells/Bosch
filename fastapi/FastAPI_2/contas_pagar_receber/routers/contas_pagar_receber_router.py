from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List, Optional
from shared.dependencies import get_db
from contas_pagar_receber.models.contas_pagar_receber_models import ContaPagarReceber
from sqlalchemy.orm import Session
from enum import Enum
from shared.exceptions import NotFound
from contas_pagar_receber.routers.fornecedor_cliente_router import FornecedorClienteResponse

router = APIRouter(prefix="/contas-pagar-receber")

class ContaPagarReceberResponse(BaseModel):
    id: int
    description: str
    value: float
    type: str
    fornecedor: FornecedorClienteResponse

    class Config:
        orm_mode = True


class ContaPagarReceberTipoEnum(str, Enum):
    PAY = 'PAY'
    RECEIVE = 'RECEIVE'


class ContaPagarReceberRequest(BaseModel):
    description: str = Field(min_length=3, max_length=30)
    value: float = Field(gt=0)
    type: ContaPagarReceberTipoEnum
    fornecedor_cliente_id: Optional[int] = None

    class Config:
        orm_mode = True


# @router.get("/", response_model=List[ContaPagarReceberResponse])
# def list_accounts():
#     return [
#         ContaPagarReceberResponse(
#             id = 1,
#             description = "Rent",
#             value = 1000.50,
#             type = "PAY"

#         ),
#         ContaPagarReceberResponse(
#             id = 2,
#             description = "Bought",
#             value = 5000,
#             type = "SELL"

#         ),
#     ]


@router.get("/", response_model=List[ContaPagarReceberResponse])
def list_accounts(db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()


@router.get("/{id_conta_pagar_receber}", response_model=ContaPagarReceberResponse)
def get_account(
        id_conta_pagar_receber: int, 
        db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    
    conta_pagar_receber = search_account_by_id(id_conta_pagar_receber, db)
    
    return conta_pagar_receber


@router.post('/', response_model=ContaPagarReceberResponse, status_code=201)
def create_account(account: ContaPagarReceberRequest, 
                   db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    
    # contas_pagar_receber = ContaPagarReceber(
    #     description=account.description, 
    #     value = account.value, 
    #     type=account.type
    # )

    contas_pagar_receber = ContaPagarReceber(
        **account.dict()
    )

    print(contas_pagar_receber)

    db.add(contas_pagar_receber)
    db.commit()
    db.refresh(contas_pagar_receber)
    
    # return ContaPagarReceberResponse(
    #         id = 3,
    #         description = account.description,
    #         value = account.value,
    #         type = account.type

    #     )
    return contas_pagar_receber


@router.put('/{id_conta_pagar_receber}', response_model=ContaPagarReceberResponse, status_code=200)
def update_account(
                    id_conta_pagar_receber: int,
                    conta_pagar_receber_request: ContaPagarReceberRequest, 
                    db: Session = Depends(get_db)) -> ContaPagarReceberResponse:

    conta_pagar_receber = search_account_by_id(id_conta_pagar_receber, db)

    conta_pagar_receber.type = conta_pagar_receber_request.type
    conta_pagar_receber.value = conta_pagar_receber_request.value
    conta_pagar_receber.description = conta_pagar_receber_request.description

    db.add(conta_pagar_receber)
    db.commit()
    db.refresh(conta_pagar_receber)

    return conta_pagar_receber


@router.delete('/{id_conta_pagar_receber}', status_code=204)
def delete_account(
                    id_conta_pagar_receber: int,
                    db: Session = Depends(get_db)) -> None:

    conta_pagar_receber = search_account_by_id(id_conta_pagar_receber, db)
    db.delete(conta_pagar_receber)
    db.commit()
    


# @router.post("/database")
# def create_conta_pagar_receber(conta: ContaPagarReceberRequest):
#     db = SessionLocal()
    
#     db_conta = ContaPagarReceber(description=conta.description, value=conta.value, type=conta.type)
#     db.add(db_conta)
#     db.commit()
#     db.refresh(db_conta)

#     contas = db.query(ContaPagarReceber).all()
    
#     db.close()
    
#     return contas

def search_account_by_id(id_conta_pagar_receber: int, db: Session) -> ContaPagarReceber:
    conta_pagar_receber = db.query(ContaPagarReceber).get(id_conta_pagar_receber)

    if conta_pagar_receber is None:
        raise NotFound("Conta a Pagar e Receber")

    return conta_pagar_receber