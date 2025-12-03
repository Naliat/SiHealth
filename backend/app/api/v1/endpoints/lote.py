from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Literal

from app.core.database import get_db
from app.services.lote_service import LoteService
from app.schemas.lote import LoteCreate, LoteResponse, LoteUpdate

# --- IMPORTAÇÃO DA SEGURANÇA ---
from app.core.dependecies import verificar_senha_mestra
# -------------------------------

router = APIRouter()

# --- ROTA PROTEGIDA COM SENHA ---
@router.post("/", response_model=LoteResponse, status_code=status.HTTP_201_CREATED)
def criar_lote(
    lote: LoteCreate, 
    db: Session = Depends(get_db),
    # O Guardião: Se o Header X-Admin-Pass não vier correto, a função nem roda
    autorizado: bool = Depends(verificar_senha_mestra) 
):
    service = LoteService(db)
    return service.criar_lote(lote)
# --------------------------------

@router.get("/", response_model=List[LoteResponse])
def listar_todos_lotes(
    skip: int = 0, 
    limit: int = 100,
    numero_lote: Optional[str] = Query(None, description="Filtrar por número do lote"),
    medicamento: Optional[str] = Query(None, description="Filtrar por nome do medicamento"),
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

@router.get("/{id_lote}", response_model=LoteResponse)
def obter_lote(id_lote: int, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.obter_por_id(id_lote)

@router.get("/medicamento/{id_medicamento}", response_model=List[LoteResponse])
def listar_lotes_do_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = LoteService(db)
    return service.listar_por_medicamento(id_medicamento)

# --- ROTA PROTEGIDA (OPCIONAL) ---
# Geralmente editar um lote também requer segurança
@router.put("/{id_lote}", response_model=LoteResponse)
def atualizar_lote(
    id_lote: int, 
    lote: LoteUpdate, 
    db: Session = Depends(get_db),
    autorizado: bool = Depends(verificar_senha_mestra) # Adicionei aqui também por precaução
):
    service = LoteService(db)
    return service.atualizar_lote(id_lote, lote)