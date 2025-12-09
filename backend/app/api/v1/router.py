from fastapi import APIRouter
from app.api.v1.endpoints import medicamento, lote, saida, dashboard, relatorio

api_router = APIRouter()

api_router.include_router(medicamento.router, prefix="/medicamentos", tags=["Medicamentos"])
api_router.include_router(lote.router, prefix="/lotes", tags=["Lotes"])
api_router.include_router(saida.router, prefix="/saidas", tags=["Saídas"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(relatorio.router, prefix="/relatorios", tags=["Relatórios"])