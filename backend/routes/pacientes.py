from fastapi import APIRouter, HTTPException
from odmantic import ObjectId

from models.paciente import Paciente
from database import engine


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


# -----------------------------
# CREATE
# -----------------------------
@router.post("/", response_model=Paciente)
async def criar_paciente(dados: Paciente):

    # CNS deve ser único
    existente_cns = await engine.find_one(Paciente, Paciente.CNS == dados.CNS)
    if existente_cns:
        raise HTTPException(status_code=400, detail="CNS já cadastrado")

    # CPF também deve ser único (se informado)
    if dados.cpf:
        existente_cpf = await engine.find_one(Paciente, Paciente.cpf == dados.cpf)
        if existente_cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    paciente = Paciente(
        nome=dados.nome,
        CNS=dados.CNS,
        cpf=dados.cpf,
        data_nascimento=dados.data_nascimento,
        sexo=dados.sexo,
    )

    await engine.save(paciente)
    return paciente


# -----------------------------
# LISTAR TODOS
# -----------------------------
@router.get("/", response_model=list[Paciente])
async def listar_pacientes():
    return await engine.find(Paciente)


# -----------------------------
# OBTER POR ID
# -----------------------------
@router.get("/{paciente_id}", response_model=Paciente)
async def obter_paciente(paciente_id: str):

    if not ObjectId.is_valid(paciente_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    paciente = await engine.find_one(Paciente, Paciente.id == ObjectId(paciente_id))

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    return paciente


# -----------------------------
# UPDATE
# -----------------------------
@router.put("/{paciente_id}", response_model=Paciente)
async def atualizar_paciente(paciente_id: str, dados: Paciente):

    if not ObjectId.is_valid(paciente_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    paciente = await engine.find_one(Paciente, Paciente.id == ObjectId(paciente_id))
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Atualizar CNS — deve continuar único
    if dados.CNS is not None:
        existente_cns = await engine.find_one(Paciente, Paciente.CNS == dados.CNS)
        if existente_cns and existente_cns.id != paciente.id:
            raise HTTPException(status_code=400, detail="CNS já está em uso")
        paciente.CNS = dados.CNS

    # Atualizar CPF — também deve ser único
    if dados.cpf is not None:
        existente_cpf = await engine.find_one(Paciente, Paciente.cpf == dados.cpf)
        if existente_cpf and existente_cpf.id != paciente.id:
            raise HTTPException(status_code=400, detail="CPF já está em uso")
        paciente.cpf = dados.cpf

    if dados.nome is not None:
        paciente.nome = dados.nome

    if dados.data_nascimento is not None:
        paciente.data_nascimento = dados.data_nascimento

    if dados.sexo is not None:
        paciente.sexo = dados.sexo

    await engine.save(paciente)
    return paciente


# -----------------------------
# DELETE
# -----------------------------
@router.delete("/{paciente_id}")
async def deletar_paciente(paciente_id: str):

    if not ObjectId.is_valid(paciente_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    paciente = await engine.find_one(Paciente, Paciente.id == ObjectId(paciente_id))
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    await engine.delete(paciente)
    return {"message": "Paciente deletado com sucesso"}
