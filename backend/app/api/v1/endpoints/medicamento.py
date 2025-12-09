from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Literal

from app.core.database import get_db
from app.services.medicamento_service import MedicamentoService
from app.schemas.medicamento import MedicamentoCreate, MedicamentoResponse, MedicamentoUpdate

# --- IMPORTAÇÃO DA SEGURANÇA ---
from app.core.dependecies import verificar_senha_mestra
# -------------------------------

router = APIRouter()

# --- ROTA PROTEGIDA (CRIAR) ---
# Exige o Header 'X-Admin-Pass'
@router.post("/", response_model=MedicamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_medicamento(
    medicamento: MedicamentoCreate, 
    db: Session = Depends(get_db),
    autorizado: bool = Depends(verificar_senha_mestra) # <--- Proteção aqui
):
    service = MedicamentoService(db)
    return service.criar_medicamento(medicamento)

# --- ROTAS DE LEITURA (PÚBLICAS) ---
# Não exigem senha para não travar o atendimento no balcão
@router.get("/", response_model=List[MedicamentoResponse])
def listar_medicamentos(
    skip: int = 0, 
    limit: int = 100,
    nome: Optional[str] = Query(None, description="Filtrar por nome (ex: 'Dipirona')"),
    tarja: Optional[str] = Query(None, description="Filtrar por tarja (ex: 'Vermelha', 'Preta')"),
    ordenar_por: Optional[Literal["nome", "tarja", "fabricante", "criado_em"]] = Query("nome", description="Campo para ordenar"),
    direcao: Optional[Literal["asc", "desc"]] = Query("asc", description="Ordem Crescente (asc) ou Decrescente (desc)"),
    db: Session = Depends(get_db)
):
    service = MedicamentoService(db)
    return service.listar_medicamentos(
        skip=skip, 
        limit=limit, 
        nome=nome, 
        tarja=tarja, 
        ordenar_por=ordenar_por, 
        direcao=direcao
    )

@router.get("/{id_medicamento}", response_model=MedicamentoResponse)
def obter_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = MedicamentoService(db)
    return service.obter_por_id(id_medicamento)

# --- ROTA PROTEGIDA (ATUALIZAR) ---
@router.put("/{id_medicamento}", response_model=MedicamentoResponse)
def atualizar_medicamento(
    id_medicamento: int, 
    medicamento: MedicamentoUpdate, 
    db: Session = Depends(get_db),
    autorizado: bool = Depends(verificar_senha_mestra) # <--- Proteção aqui
):
    service = MedicamentoService(db)
    return service.atualizar_medicamento(id_medicamento, medicamento)

# --- ROTA PROTEGIDA (DELETAR) ---
@router.delete("/{id_medicamento}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_medicamento(
    id_medicamento: int, 
    db: Session = Depends(get_db),
    autorizado: bool = Depends(verificar_senha_mestra) # <--- Proteção aqui
):
    service = MedicamentoService(db)
    service.deletar_medicamento(id_medicamento)