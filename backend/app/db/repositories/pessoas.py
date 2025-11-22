from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from app.schemas.usuario import UsuarioCreate
from app.schemas.paciente import PacienteCreate

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_all(self):
        return self.db.query(Usuario).all()

    def create(self, usuario: UsuarioCreate, senha_hash: str):
        # Aqui criamos o objeto manualmente para separar a senha crua do hash
        db_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            senha_hash=senha_hash, # Salva o hash, não a senha real
            ativo=usuario.ativo
        )
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

class PacienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cns(self, cns: str):
        return self.db.query(Paciente).filter(Paciente.cns == cns).first()
    
    def get_all(self):
        return self.db.query(Paciente).all()

    def create(self, paciente: PacienteCreate):
        db_paciente = Paciente(**paciente.model_dump())
        self.db.add(db_paciente)
        self.db.commit()
        self.db.refresh(db_paciente)
        return db_paciente