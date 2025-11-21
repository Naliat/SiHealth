from fastapi import APIRouter, Depends, HTTPException
from typing import List
from odmantic import AIOEngine, ObjectId

from models.medicamento import Medicamento
from models.lote import Lote
from models.medicamento_completo import Medicamento_completo

from database import engine



router = APIRouter(
    prefix="/medicamentos",
    tags=["Medicamentos"]
)

@router.get("/completo", response_model=list[Medicamento_completo])
async def listar_com_info_completa():
    remedios = await engine.find(Medicamento)
    resposta = []

    for r in remedios:
        lote = await engine.find_one(Lote, Lote.id_medicamento == r.id)

        resposta.append({
            "id": str(r.id),
            "nome": r.nome,
            "principio_ativo": r.principio_ativo,
            "dosagem": r.dosagem,
            "fabricante": r.fabricante,

            "numero_da_caixa": lote.numero_caixa if lote else None,
            "lote": lote.numero_lote if lote else None,
            "validade": lote.data_validade.date().isoformat() if lote else None,
            "quantidade": lote.quantidade_atual if lote else None,
            "quantidade_por_caixa": lote.quantidade_por_caixa if lote else None
        })

    return resposta


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

# -------------------------------
# saida do medicamento completo
# -------------------------------




