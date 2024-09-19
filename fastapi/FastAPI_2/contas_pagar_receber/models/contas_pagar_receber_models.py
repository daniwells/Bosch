from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from shared.database import Base

class ContaPagarReceber(Base):
    __tablename__ = "contas_pagar_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(30))
    value = Column(Numeric)
    type = Column(String(30))

    fornecedor_cliente_id = Column(Integer, ForeignKey("fornecedor_cliente.id"))
    fornecedor = relationship("FornecedorCliente")