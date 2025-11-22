from sqlalchemy.orm import Session
from app.models.medicamento import Medicamento
from app.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate

class MedicamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_medicamento: int):
        return self.db.query(Medicamento).filter(Medicamento.id_medicamento == id_medicamento).first()

    def get_by_nome(self, nome: str):
        # Útil para evitar duplicatas
        return self.db.query(Medicamento).filter(Medicamento.nome == nome).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Medicamento).offset(skip).limit(limit).all()

    def create(self, medicamento: MedicamentoCreate):
        # Converte o schema Pydantic para o modelo SQLAlchemy
        db_medicamento = Medicamento(**medicamento.model_dump())
        
        self.db.add(db_medicamento)
        self.db.commit()
        self.db.refresh(db_medicamento) # Atualiza o objeto com o ID gerado pelo banco
        return db_medicamento

    def update(self, db_medicamento: Medicamento, medicamento_update: MedicamentoUpdate):
        # Pegamos apenas os dados que foram enviados (exclui os nulos)
        update_data = medicamento_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_medicamento, key, value)

        self.db.add(db_medicamento)
        self.db.commit()
        self.db.refresh(db_medicamento)
        return db_medicamento
    
    def delete(self, db_medicamento: Medicamento):
        self.db.delete(db_medicamento)
        self.db.commit()