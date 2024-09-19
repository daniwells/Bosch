import uvicorn
from fastapi import FastAPI
from contas_pagar_receber.routers import contas_pagar_receber_router, fornecedor_cliente_router
from shared.database import engine, Base
# from contas_pagar_receber.models.contas_pagar_receber_models import ContaPagarReceber

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler

app = FastAPI()

@app.get("/")
def hello_world() -> str:
    return "Hello World!"

app.include_router(contas_pagar_receber_router.router)
app.include_router(fornecedor_cliente_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)