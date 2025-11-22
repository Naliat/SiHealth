from sqlalchemy.orm import Session
from app.models.entrada import Entrada
from app.models.saida import Saida
from app.schemas.entrada import EntradaCreate
from app.schemas.saida import SaidaCreate

class EntradaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, entrada: EntradaCreate):
        db_entrada = Entrada(**entrada.model_dump())
        self.db.add(db_entrada)
        # O commit será feito no Service para garantir a transação completa (entrada + atualização de estoque)
        return db_entrada

class SaidaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, saida: SaidaCreate, total_calculado: int):
        # Removemos campos que não existem na tabela (calculados) e adicionamos o total
        dados = saida.model_dump()
        
        db_saida = Saida(
            **dados,
            quantidade_total_entregue=total_calculado
        )
        self.db.add(db_saida)
        return db_saida