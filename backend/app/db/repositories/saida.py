# app/db/repositories/saida.py
from sqlalchemy.orm import Session
from app.models.saida import Saida

class SaidaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, saida: Saida):
        self.db.add(saida)
        # O commit será feito no Service para garantir a transação
        return saida