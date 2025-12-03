from fastapi import APIRouter
from app.api.v1.endpoints import medicamento, lote, saida

api_router = APIRouter()

api_router.include_router(medicamento.router, prefix="/medicamentos", tags=["Medicamentos"])
api_router.include_router(lote.router, prefix="/lotes", tags=["Lotes"])
api_router.include_router(saida.router, prefix="/saidas", tags=["Saídas"])