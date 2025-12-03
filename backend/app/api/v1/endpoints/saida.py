# app/api/v1/endpoints/saida.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.saida_service import SaidaService
from app.schemas.saida import SaidaCreate, SaidaResponse

# Importe sua nova dependência
from app.core.dependecies import verificar_senha_mestra

router = APIRouter()

@router.post("/", response_model=SaidaResponse, status_code=status.HTTP_201_CREATED)
def registrar_saida(
    saida: SaidaCreate, 
    db: Session = Depends(get_db),
    # --- O GUARDIÃO ---
    # Ao adicionar esta linha, o FastAPI exige o Header X-Admin-Pass
    autorizado: bool = Depends(verificar_senha_mestra) 
):
    service = SaidaService(db)
    # Não precisamos mais passar ID de usuário ou senha para o service
    return service.registrar_saida(saida)