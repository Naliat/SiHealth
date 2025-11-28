from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Literal

from app.core.database import get_db
from app.services.medicamento_service import MedicamentoService
from app.schemas.medicamento import MedicamentoCreate, MedicamentoResponse, MedicamentoUpdate

router = APIRouter()

@router.post("/", response_model=MedicamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    service = MedicamentoService(db)
    return service.criar_medicamento(medicamento)

# --- ROTA LISTAR ATUALIZADA ---
@router.get("/", response_model=List[MedicamentoResponse])
def listar_medicamentos(
    skip: int = 0, 
    limit: int = 100,
    # Filtros
    nome: Optional[str] = Query(None, description="Filtrar por nome (ex: 'Dipirona')"),
    tarja: Optional[str] = Query(None, description="Filtrar por tarja (ex: 'Vermelha', 'Preta')"),
    
    # Ordenação (Dropdown no Swagger)
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
# -----------------------------

@router.get("/{id_medicamento}", response_model=MedicamentoResponse)
def obter_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = MedicamentoService(db)
    return service.obter_por_id(id_medicamento)

@router.put("/{id_medicamento}", response_model=MedicamentoResponse)
def atualizar_medicamento(id_medicamento: int, medicamento: MedicamentoUpdate, db: Session = Depends(get_db)):
    service = MedicamentoService(db)
    return service.atualizar_medicamento(id_medicamento, medicamento)

@router.delete("/{id_medicamento}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = MedicamentoService(db)
    service.deletar_medicamento(id_medicamento)