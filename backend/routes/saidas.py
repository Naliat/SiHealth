from fastapi import APIRouter, HTTPException
from odmantic import AIOEngine, ObjectId
from database import engine

from models.saida import Saida
router = APIRouter(prefix="/saidas", tags=["Saídas"])

# 📌 CREATE
@router.post("/", response_model=Saida)
async def criar_saida(data: Saida):
    saida = Saida(
        id_lote=ObjectId(data.id_lote),
        id_paciente=ObjectId(data.id_paciente),
        id_usuario_responsavel=ObjectId(data.id_usuario_responsavel),

        numero_de_caixas_entregues=data.numero_de_caixas_entregues,
        quantidade_por_caixa=data.quantidade_por_caixa,
        quantidade_total_entregue=(
            data.numero_de_caixas_entregues * data.quantidade_por_caixa
        ),
        observacao=data.observacao,
    )

    saved = await engine.save(saida)
    return saved


# 📌 READ – Todos
@router.get("/", response_model=list[Saida])
async def listar_saidas():
    return await engine.find(Saida)


# 📌 READ – Por ID
@router.get("/{saida_id}", response_model=Saida)
async def obter_saida(saida_id: str):
    saida = await engine.find_one(Saida, Saida.id == ObjectId(saida_id))
    if not saida:
        raise HTTPException(404, "Saída não encontrada.")
    return saida


# 📌 UPDATE
@router.put("/{saida_id}", response_model=Saida)
async def atualizar_saida(saida_id: str, data: Saida):
    saida = await engine.find_one(Saida, Saida.id == ObjectId(saida_id))
    if not saida:
        raise HTTPException(404, "Saída não encontrada.")

    if data.numero_de_caixas_entregues is not None:
        saida.numero_de_caixas_entregues = data.numero_de_caixas_entregues

    if data.quantidade_por_caixa is not None:
        saida.quantidade_por_caixa = data.quantidade_por_caixa

    # Recalcula automaticamente
    saida.quantidade_total_entregue = (
        saida.numero_de_caixas_entregues * saida.quantidade_por_caixa
    )

    if data.observacao is not None:
        saida.observacao = data.observacao

    updated = await engine.save(saida)
    return updated


# 📌 DELETE
@router.delete("/{saida_id}")
async def deletar_saida(saida_id: str):
    saida = await engine.find_one(Saida, Saida.id == ObjectId(saida_id))
    if not saida:
        raise HTTPException(404, "Saída não encontrada.")

    await engine.delete(saida)
    return {"message": "Saída removida com sucesso."}
