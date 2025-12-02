from fastapi import APIRouter
from app.api.v1.endpoints import medicamento, lote, movimentacao, admin, dashboard

api_router = APIRouter()

# Inclui as rotas com prefixos e tags (para organização no Swagger)
api_router.include_router(medicamento.router, prefix="/medicamentos", tags=["Medicamentos"])
api_router.include_router(lote.router, prefix="/lotes", tags=["Lotes"])
api_router.include_router(movimentacao.router, prefix="/movimentacao", tags=["Movimentação de Estoque"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administração (Cadastros)"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])