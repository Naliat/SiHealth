from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services import MedicamentoService
from app.schemas.medicamento import MedicamentoCreate, MedicamentoResponse, MedicamentoUpdate

router = APIRouter()

@router.post("/", response_model=MedicamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_medicamento(
    medicamento: MedicamentoCreate, 
    db: Session = Depends(get_db)
):
    service = MedicamentoService(db)
    return service.criar_medicamento(medicamento)

@router.get("/", response_model=List[MedicamentoResponse])
def listar_medicamentos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    service = MedicamentoService(db)
    return service.listar_medicamentos(skip, limit)

@router.get("/{id_medicamento}", response_model=MedicamentoResponse)
def obter_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = MedicamentoService(db)
    return service.obter_por_id(id_medicamento)

@router.put("/{id_medicamento}", response_model=MedicamentoResponse)
def atualizar_medicamento(
    id_medicamento: int, 
    medicamento: MedicamentoUpdate, 
    db: Session = Depends(get_db)
):
    service = MedicamentoService(db)
    return service.atualizar_medicamento(id_medicamento, medicamento)

@router.delete("/{id_medicamento}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    service = MedicamentoService(db)
    service.deletar_medicamento(id_medicamento)
    # 204 No Content não retorna corpo