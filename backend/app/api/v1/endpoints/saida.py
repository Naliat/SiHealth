# app/api/v1/endpoints/saida.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.saida_service import SaidaService
from app.schemas.saida import SaidaCreate, SaidaResponse

router = APIRouter()

@router.post("/", response_model=SaidaResponse, status_code=status.HTTP_201_CREATED)
def registrar_saida(
    saida: SaidaCreate, 
    db: Session = Depends(get_db)
):
    service = SaidaService(db)
    return service.registrar_saida(saida)