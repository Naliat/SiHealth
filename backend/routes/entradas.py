from fastapi import APIRouter, HTTPException
from odmantic import AIOEngine
from bson import ObjectId
from database import engine
from models.entrada import Entrada
router = APIRouter(prefix="/entradas", tags=["Entradas"])




# ------------------------
# CREATE
# ------------------------
@router.post("/", response_model=Entrada)
async def criar_entrada(dados: Entrada):
    entrada = Entrada(
        id_lote=ObjectId(dados.id_lote),
        id_usuario=ObjectId(dados.id_usuario),
        quantidade=dados.quantidade,
        fornecedor=dados.fornecedor,
    )
    await engine.save(entrada)

    return Entrada(
        id_entrada=str(entrada.id),
        id_lote=str(entrada.id_lote),
        id_usuario=str(entrada.id_usuario),
        quantidade=entrada.quantidade,
        data_entrada=entrada.data_entrada,
        fornecedor=entrada.fornecedor
    )


# ------------------------
# LISTAR TODAS
# ------------------------

@router.get("/", response_model=list[Entrada])
async def listar_medicamentos():
    medicamentos = await engine.find(Entrada)
    return medicamentos

# ------------------------
# BUSCAR POR ID
# ------------------------
@router.get("/{id_entrada}")
async def obter_entrada(id_entrada: str):
    try:
        obj_id = ObjectId(id_entrada)
    except:
        raise HTTPException(400, "ID inválido")

    entrada = await engine.find_one(Entrada, Entrada.id == obj_id)

    if not entrada:
        raise HTTPException(404, "Entrada não encontrada")

    return entrada



# ------------------------
# UPDATE
# ------------------------
@router.put("/{id_entrada}", response_model=Entrada)
async def atualizar_entrada(id_entrada: str, dados: Entrada):
    entrada = await engine.find_one(Entrada, Entrada.id == ObjectId(id_entrada))
    if not entrada:
        raise HTTPException(404, "Entrada não encontrada")

    entrada.id_lote = ObjectId(dados.id_lote)
    entrada.id_usuario = ObjectId(dados.id_usuario)
    entrada.quantidade = dados.quantidade
    entrada.fornecedor = dados.fornecedor

    await engine.save(entrada)

    return Entrada(
        id_entrada=str(entrada.id),
        id_lote=str(entrada.id_lote),
        id_usuario=str(entrada.id_usuario),
        quantidade=entrada.quantidade,
        data_entrada=entrada.data_entrada,
        fornecedor=entrada.fornecedor
    )


# ------------------------
# DELETE
# ------------------------
@router.delete("/{id_entrada}")
async def deletar_entrada(id_entrada: str):
    entrada = await engine.find_one(Entrada, Entrada.id == ObjectId(id_entrada))
    if not entrada:
        raise HTTPException(404, "Entrada não encontrada")

    await engine.delete(entrada)

    return {"msg": "Entrada deletada com sucesso!"}
