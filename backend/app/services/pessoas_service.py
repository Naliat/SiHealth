from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.db.repositories import UsuarioRepository, PacienteRepository
from app.schemas.usuario import UsuarioCreate
from app.schemas.paciente import PacienteCreate

# Configuração do Hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def criar_usuario(self, dados: UsuarioCreate):
        if self.repo.get_by_email(dados.email):
             raise HTTPException(status_code=400, detail="Email já cadastrado.")
        
        # Gera o hash da senha
        senha_hash = pwd_context.hash(dados.senha)
        
        return self.repo.create(dados, senha_hash)
    
    def listar_usuarios(self):
        return self.repo.get_all()

class PacienteService:
    def __init__(self, db: Session):
        self.repo = PacienteRepository(db)

    def criar_paciente(self, dados: PacienteCreate):
        if self.repo.get_by_cns(dados.cns):
             raise HTTPException(status_code=400, detail="Paciente com este CNS já existe.")
        
        return self.repo.create(dados)
    
    def listar_pacientes(self):
        return self.repo.get_all()