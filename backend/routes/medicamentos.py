from fastapi import APIRouter, HTTPException
from typing import List
from odmantic import ObjectId

from models.medicamento import Medicamento
from database import engine

router = APIRouter(
    prefix="/medicamentos",
    tags=["Medicamentos"]
)

# -------------------------------
# Criar medicamento
# -------------------------------
@router.post("/", response_model=Medicamento)
async def criar_medicamento(medicamento: Medicamento):
    novo_medicamento = await engine.save(medicamento)
    return novo_medicamento

# -------------------------------
# Listar todos
# -------------------------------
@router.get("/", response_model=List[Medicamento])
async def listar_medicamentos():
    medicamentos = await engine.find(Medicamento)
    return medicamentos

# -------------------------------
# Buscar um medicamento por ID
# -------------------------------
@router.get("/{med_id}", response_model=Medicamento)
async def obter_medicamento(med_id: str):
    medicamento = await engine.find_one(Medicamento, Medicamento.id == ObjectId(med_id))

    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    return medicamento

# -------------------------------
# Atualizar medicamento
# -------------------------------
@router.put("/{med_id}", response_model=Medicamento)
async def update_medicamento(med_id: str, data: Medicamento):
    medicamento = await engine.find_one(Medicamento, Medicamento.id == ObjectId(med_id))

    if not medicamento:
        raise HTTPException(404, "Medicamento não encontrado")

    # Atualiza apenas os campos enviados
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medicamento, field, value)

    # Salva o mesmo objeto → o mesmo ID é mantido
    await engine.save(medicamento)

    return medicamento

# -------------------------------
# Deletar medicamento
# -------------------------------
@router.delete("/{med_id}")
async def deletar_medicamento(med_id: str):
    medicamento = await engine.find_one(Medicamento, Medicamento.id == ObjectId(med_id))

    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    await engine.delete(medicamento)
    return {"detail": "Medicamento deletado com sucesso"}
