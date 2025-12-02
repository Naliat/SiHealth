from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from app.db.repositories import LoteRepository, MedicamentoRepository
from app.schemas.lote import LoteCreate, LoteUpdate

class LoteService:
    def __init__(self, db: Session):
        self.lote_repo = LoteRepository(db)
        self.medicamento_repo = MedicamentoRepository(db)

    # --- ADICIONE ESTE MÉTODO ---
    def listar_todos(self, skip: int = 0, limit: int = 100):
        # Chama o get_all do repositório (que já tem o joinedload configurado)
        return self.lote_repo.get_all(skip, limit)
    # ----------------------------

    def criar_lote(self, dados: LoteCreate):
        medicamento = self.medicamento_repo.get_by_id(dados.id_medicamento)
        if not medicamento:
            raise HTTPException(status_code=404, detail=f"Medicamento {dados.id_medicamento} não encontrado.")
        
        if dados.data_validade < date.today():
             raise HTTPException(status_code=400, detail="Data de validade inválida.")

        return self.lote_repo.create(dados)

    def obter_por_id(self, id_lote: int):
        lote = self.lote_repo.get_by_id(id_lote)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote não encontrado.")
        return lote

    def listar_por_medicamento(self, id_medicamento: int):
        if not self.medicamento_repo.get_by_id(id_medicamento):
             raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
        return self.lote_repo.get_by_medicamento(id_medicamento)
    
    def atualizar_lote(self, id_lote: int, dados: LoteUpdate):
        lote = self.obter_por_id(id_lote)
        return self.lote_repo.update(lote, dados)