from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.movimentacao_service import MovimentacaoService
from app.schemas.entrada import EntradaCreate, EntradaResponse
from app.schemas.saida import SaidaCreate, SaidaResponse

router = APIRouter()

@router.post("/entrada", response_model=EntradaResponse, status_code=status.HTTP_201_CREATED)
def realizar_entrada(entrada: EntradaCreate, db: Session = Depends(get_db)):
    service = MovimentacaoService(db)
    return service.registrar_entrada(entrada)

@router.post("/saida", response_model=SaidaResponse, status_code=status.HTTP_201_CREATED)
def realizar_saida(saida: SaidaCreate, db: Session = Depends(get_db)):
    service = MovimentacaoService(db)
    return service.registrar_saida(saida)