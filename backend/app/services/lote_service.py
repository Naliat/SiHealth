from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from app.db.repositories import LoteRepository, MedicamentoRepository
from app.schemas.lote import LoteCreate, LoteUpdate

class LoteService:
    def __init__(self, db: Session):
        self.lote_repo = LoteRepository(db)
        self.medicamento_repo = MedicamentoRepository(db)

    def criar_lote(self, dados: LoteCreate):
        # Validação: O medicamento existe?
        medicamento = self.medicamento_repo.get_by_id(dados.id_medicamento)
        if not medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento com ID {dados.id_medicamento} não encontrado. Não é possível criar o lote."
            )

        # Validação: Data de validade não pode ser no passado
        if dados.data_validade < date.today():
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de validade não pode ser anterior à data de hoje."
            )

        return self.lote_repo.create(dados)

    def obter_por_id(self, id_lote: int):
        lote = self.lote_repo.get_by_id(id_lote)
        if not lote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lote não encontrado."
            )
        return lote

    def listar_por_medicamento(self, id_medicamento: int):
        # Verifica se o medicamento existe antes de buscar os lotes
        if not self.medicamento_repo.get_by_id(id_medicamento):
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medicamento não encontrado."
            )
        return self.lote_repo.get_by_medicamento(id_medicamento)
    
    def atualizar_lote(self, id_lote: int, dados: LoteUpdate):
        lote = self.obter_por_id(id_lote)
        return self.lote_repo.update(lote, dados)