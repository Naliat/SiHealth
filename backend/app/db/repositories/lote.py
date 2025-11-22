from sqlalchemy.orm import Session
from app.models.lote import Lote
from app.schemas.lote import LoteCreate, LoteUpdate

class LoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_lote: int):
        return self.db.query(Lote).filter(Lote.id_lote == id_lote).first()

    def get_by_medicamento(self, id_medicamento: int):
        # Retorna todos os lotes de um remédio específico
        return self.db.query(Lote).filter(Lote.id_medicamento == id_medicamento).all()

    def create(self, lote: LoteCreate):
        # Regra: Ao criar, a quantidade atual é igual à inicial
        dados_lote = lote.model_dump()
        
        # Cria o objeto Lote forçando a quantidade_atual
        db_lote = Lote(
            **dados_lote,
            quantidade_atual=lote.quantidade_inicial 
        )
        
        self.db.add(db_lote)
        self.db.commit()
        self.db.refresh(db_lote)
        return db_lote

    def update(self, db_lote: Lote, lote_update: LoteUpdate):
        update_data = lote_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_lote, key, value)

        self.db.add(db_lote)
        self.db.commit()
        self.db.refresh(db_lote)
        return db_lote

    # Método extra útil para baixar estoque
    def atualizar_estoque(self, id_lote: int, quantidade_retirada: int):
        db_lote = self.get_by_id(id_lote)
        if db_lote and db_lote.quantidade_atual >= quantidade_retirada:
            db_lote.quantidade_atual -= quantidade_retirada
            self.db.commit()
            self.db.refresh(db_lote)
            return db_lote
        return None # Ou levantar erro de estoque insuficiente