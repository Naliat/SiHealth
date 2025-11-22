from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.repositories import MedicamentoRepository
from app.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate

class MedicamentoService:
    def __init__(self, db: Session):
        self.medicamento_repo = MedicamentoRepository(db)

    def criar_medicamento(self, dados: MedicamentoCreate):
        # Regra de Negócio: Verificar duplicidade pelo nome
        if self.medicamento_repo.get_by_nome(dados.nome):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um medicamento cadastrado com este nome."
            )
        
        return self.medicamento_repo.create(dados)

    def listar_medicamentos(self, skip: int = 0, limit: int = 100):
        return self.medicamento_repo.get_all(skip, limit)

    def obter_por_id(self, id_medicamento: int):
        medicamento = self.medicamento_repo.get_by_id(id_medicamento)
        if not medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medicamento não encontrado."
            )
        return medicamento

    def atualizar_medicamento(self, id_medicamento: int, dados: MedicamentoUpdate):
        medicamento = self.obter_por_id(id_medicamento) # Já valida se existe (404)
        return self.medicamento_repo.update(medicamento, dados)

    def deletar_medicamento(self, id_medicamento: int):
        medicamento = self.obter_por_id(id_medicamento) # Já valida se existe (404)
        self.medicamento_repo.delete(medicamento)