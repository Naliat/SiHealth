from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services import LoteService
from app.schemas.lote import LoteCreate, LoteResponse, LoteUpdate

router = APIRouter()

# --- NOVA ROTA: LISTAR TODOS OS LOTES ---
@router.get("/", response_model=List[LoteResponse])
def listar_todos_lotes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    service = LoteService(db)
    return service.listar_todos(skip, limit)
# ----------------------------------------

@router.post("/", response_model=LoteResponse, status_code=status.HTTP_201_CREATED)
def criar_lote(lote: LoteCreate, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.criar_lote(lote)

@router.get("/{id_lote}", response_model=LoteResponse)
def obter_lote(id_lote: int, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.obter_por_id(id_lote)

# Rota específica para lotes de UM medicamento
@router.get("/medicamento/{id_medicamento}", response_model=List[LoteResponse])
def listar_lotes_do_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.listar_por_medicamento(id_medicamento)

@router.put("/{id_lote}", response_model=LoteResponse)
def atualizar_lote(id_lote: int, lote: LoteUpdate, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.atualizar_lote(id_lote, lote)