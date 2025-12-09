from sqlalchemy.orm import Session
from datetime import date
from fastapi import HTTPException

from app.db.repositories.relatorio import RelatorioRepository

class RelatorioService:
    def __init__(self, db: Session):
        self.repo = RelatorioRepository(db)

    def obter_dados_completos(self, inicio: date, fim: date):
        if inicio > fim:
            raise HTTPException(status_code=400, detail="Data inicial inválida.")
        
        # Busca as duas partes do relatório
        estoque = self.repo.buscar_estoque_total()
        dispensacoes = self.repo.buscar_dispensacoes(inicio, fim)
        
        return estoque, dispensacoes