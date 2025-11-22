# main.py
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
# Import necessário para criar tabelas
import app.models 
from app.api.v1.router import api_router

# Cria as tabelas (caso ainda não existam)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_TITLE,
    version="1.0.0",
    description="API de Gerenciamento de Estoque Farmacêutico - SiHealth",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Conecta o roteador principal da V1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Status"])
def health_check():
    return {"status": "ok", "mensagem": "API SiHealth rodando!"}