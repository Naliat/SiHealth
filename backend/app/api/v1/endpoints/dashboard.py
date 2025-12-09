# app/api/v1/endpoints/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import DashboardResponse

router = APIRouter()

@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    """
    Retorna todos os indicadores para a tela inicial (Dashboard).
    """
    service = DashboardService(db)
    return service.obter_dados_dashboard()