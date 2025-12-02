from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import DashboardResponse

router = APIRouter()

@router.get("/", response_model=DashboardResponse)
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Retorna todos os dados para montar a tela de Dashboard:
    KPIs, Gráficos e Tabelas de Alerta.
    """
    service = DashboardService(db)
    return service.obter_dados_gerais()