from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from passlib.hash import bcrypt

from models.usuario import Usuario
from database import engine

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


# -----------------------------
# CREATE
# -----------------------------
@router.post("/", response_model=Usuario)
async def criar_usuario(dados: Usuario):
    # Verifica se já existe email
    existente = await engine.find_one(Usuario, Usuario.email == dados.email)
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    senha_hash = bcrypt.hash(dados.senha_hash)

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=senha_hash,
    )

    await engine.save(usuario)
    return usuario


# -----------------------------
# LISTAR TODOS
# -----------------------------
@router.get("/", response_model=list[Usuario])
async def listar_usuarios():
    usuarios = await engine.find(Usuario)
    return usuarios


# -----------------------------
# OBTER POR ID
# -----------------------------
@router.get("/{usuario_id}", response_model=Usuario)
async def obter_usuario(usuario_id: str):
    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


# -----------------------------
# UPDATE
# -----------------------------
@router.put("/{usuario_id}", response_model=Usuario)
async def atualizar_usuario(usuario_id: str, dados: Usuario):

    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    existente = await engine.find_one(Usuario, Usuario.email == dados.email)
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Atualiza apenas campos enviados
    if dados.nome is not None:
        usuario.nome = dados.nome

    if dados.email is not None:
        # Verifica se email já existe
        existente = await engine.find_one(Usuario, Usuario.email == dados.email)
        if existente and existente.id != usuario.id:
            raise HTTPException(status_code=400, detail="Email já em uso")
        usuario.email = dados.email

    if dados.senha_hash is not None:
        usuario.senha_hash = bcrypt.hash(dados.senha_hash)

    await engine.save(usuario)
    return usuario


# -----------------------------
# DELETE
# -----------------------------
@router.delete("/{usuario_id}")
async def deletar_usuario(usuario_id: str):

    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    await engine.delete(usuario)

    return {"message": "Usuário deletado com sucesso"}
