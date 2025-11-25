from sqlalchemy.orm import Session, joinedload # <--- Não esqueça do import
from sqlalchemy import asc, desc
from app.models.lote import Lote
from app.schemas.lote import LoteCreate, LoteUpdate

class LoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        # --- ADICIONE O joinedload AQUI ---
        return (
            self.db.query(Lote)
            .options(joinedload(Lote.medicamento)) # Carrega os dados do medicamento
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, id_lote: int):
        # --- AQUI TAMBÉM ---
        return (
            self.db.query(Lote)
            .options(joinedload(Lote.medicamento))
            .filter(Lote.id_lote == id_lote)
            .first()
        )

    def get_by_medicamento(self, id_medicamento: int):
        return (
            self.db.query(Lote)
            .options(joinedload(Lote.medicamento))
            .filter(Lote.id_medicamento == id_medicamento)
            .all()
        )

    # ... (Create, Update e outros métodos mantêm a lógica, 
    # mas lembre-se que o Create retorna o objeto criado. 
    # Se quiser que o retorno do POST já venha com o medicamento, 
    # precisaria fazer um refresh mais complexo, mas geralmente não precisa).

    def create(self, lote: LoteCreate):
        # ... seu código de create ...
        # DICA: O Lote recém-criado pode não ter o relacionamento carregado.
        # Se der erro no retorno do POST, o jeito mais simples é:
        db_lote = Lote(**dados_lote, quantidade_atual=lote.quantidade_inicial)
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