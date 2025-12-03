from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.pessoas_service import UsuarioService, PacienteService
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.paciente import PacienteCreate, PacienteResponse

router = APIRouter()
"""
# --- Rotas de Usuário ---
@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.criar_usuario(usuario)

@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.listar_usuarios()
"""
# --- Rotas de Paciente ---
@router.post("/pacientes", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    service = PacienteService(db)
    return service.criar_paciente(paciente)

@router.get("/pacientes", response_model=List[PacienteResponse])
def listar_pacientes(db: Session = Depends(get_db)):
    service = PacienteService(db)
    return service.listar_pacientes()