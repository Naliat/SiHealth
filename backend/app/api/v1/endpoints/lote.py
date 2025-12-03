# app/api/v1/endpoints/lote.py
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Literal

from app.core.database import get_db
from app.services.lote_service import LoteService
from app.schemas.lote import LoteCreate, LoteResponse, LoteUpdate

router = APIRouter()

@router.get("/", response_model=List[LoteResponse])
def listar_todos_lotes(
    skip: int = 0, 
    limit: int = 100,
    # Filtros Opcionais
    numero_lote: Optional[str] = Query(None, description="Filtrar por número do lote (ex: 'L2024')"),
    medicamento: Optional[str] = Query(None, description="Filtrar por nome do medicamento (ex: 'Dipirona')"),
    
    # Ordenação
    ordenar_por: Optional[Literal["numero_lote", "validade", "quantidade", "medicamento", "criado_em"]] = Query("validade", description="Campo para ordenar"),
    direcao: Optional[Literal["asc", "desc"]] = Query("asc", description="Direção da ordenação"),
    
    db: Session = Depends(get_db)
):
    service = LoteService(db)
    return service.listar_todos(
        skip=skip, 
        limit=limit,
        numero_lote=numero_lote,
        nome_medicamento=medicamento,
        ordenar_por=ordenar_por,
        direcao=direcao
    )

# ... (Mantenha as outras rotas POST, GET /{id}, PUT, DELETE como estavam) ...
@router.post("/", response_model=LoteResponse, status_code=status.HTTP_201_CREATED)
def criar_lote(lote: LoteCreate, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.criar_lote(lote)

@router.get("/{id_lote}", response_model=LoteResponse)
def obter_lote(id_lote: int, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.obter_por_id(id_lote)

@router.get("/medicamento/{id_medicamento}", response_model=List[LoteResponse])
def listar_lotes_do_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.listar_por_medicamento(id_medicamento)

@router.put("/{id_lote}", response_model=LoteResponse)
def atualizar_lote(id_lote: int, lote: LoteUpdate, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.atualizar_lote(id_lote, lote)