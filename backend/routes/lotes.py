# routers/lote.py
from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine
from database import engine
from models.lote import Lote
from bson import ObjectId

router = APIRouter(prefix="/lotes", tags=["Lotes"])


# Dependência
async def get_engine() -> AIOEngine:
    return engine


# Criar Lote
@router.post("/", response_model=Lote)
async def criar_lote(lote_data: Lote, engine: AIOEngine = Depends(get_engine)):

    # Verifica se existe numero_lote duplicado
    existe = await engine.find_one(Lote, Lote.numero_lote == lote_data.numero_lote)
    if existe:
        raise HTTPException(400, "Já existe um lote com esse número.")

    lote = Lote(
        id_medicamento=ObjectId(lote_data.id_medicamento),
        numero_lote=lote_data.numero_lote,
        numero_caixa=lote_data.numero_caixa,
        quantidade_por_caixa=lote_data.quantidade_por_caixa,
        quantidade_inicial=lote_data.quantidade_inicial,
        quantidade_atual=lote_data.quantidade_atual,
        data_fabricacao=lote_data.data_fabricacao,
        data_validade=lote_data.data_validade,
    )

    await engine.save(lote)
    return lote


# Listar todos os lotes
@router.get("/", response_model=list[Lote])
async def listar_lotes(engine: AIOEngine = Depends(get_engine)):
    return await engine.find(Lote)


# Buscar por ID
@router.get("/{lote_id}", response_model=Lote)
async def buscar_lote(id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        oid = ObjectId(id)
    except:
        raise HTTPException(400, "ID inválido")

    lote = await engine.find_one(Lote, Lote.id == oid)
    if not lote:
        raise HTTPException(404, "Lote não encontrado.")

    return lote


# Atualizar Lote
@router.put("/{lote_id}", response_model=Lote)
async def atualizar_lote(id: str, lote_data: Lote, engine: AIOEngine = Depends(get_engine)):
    try:
        oid = ObjectId(id)
    except:
        raise HTTPException(400, "ID inválido")

    lote = await engine.find_one(Lote, Lote.id == oid)
    if not lote:
        raise HTTPException(404, "Lote não encontrado.")

    lote.id_medicamento = ObjectId(lote_data.id_medicamento)
    lote.numero_lote = lote_data.numero_lote
    lote.numero_caixa = lote_data.numero_caixa
    lote.quantidade_por_caixa = lote_data.quantidade_por_caixa
    lote.quantidade_inicial = lote_data.quantidade_inicial
    lote.quantidade_atual = lote_data.quantidade_atual
    lote.data_fabricacao = lote_data.data_fabricacao
    lote.data_validade = lote_data.data_validade

    await engine.save(lote)
    return lote


# Deletar Lote
@router.delete("/{lote_id}")
async def deletar_lote(id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        oid = ObjectId(id)
    except:
        raise HTTPException(400, "ID inválido")

    lote = await engine.find_one(Lote, Lote.id == oid)
    if not lote:
        raise HTTPException(404, "Lote não encontrado.")

    await engine.delete(lote)
    return {"detail": "Lote deletado com sucesso."}
