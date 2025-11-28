from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from app.models.medicamento import Medicamento
from app.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate

class MedicamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        nome_filtro: str = None, 
        tarja_filtro: str = None, 
        ordenar_por: str = None, 
        direcao: str = "asc"
    ):
        # --- MUDANÇA IMPORTANTE AQUI ---
        # Adicionamos .options(joinedload(Medicamento.lotes))
        # Isso traz os lotes junto com o remédio para podermos calcular a validade
        query = self.db.query(Medicamento).options(joinedload(Medicamento.lotes))
        # -------------------------------

        # --- FILTROS ---
        
        # 1. Filtro por Nome (Parcial)
        if nome_filtro:
            query = query.filter(Medicamento.nome.ilike(f"%{nome_filtro}%"))

        # 2. Filtro por Tarja (Exato ou Parcial)
        if tarja_filtro:
            query = query.filter(Medicamento.tarja.ilike(f"%{tarja_filtro}%"))

        # --- ORDENAÇÃO ---
        
        if ordenar_por:
            campo_ordenacao = None
            
            if ordenar_por == "nome":
                campo_ordenacao = Medicamento.nome
            elif ordenar_por == "tarja":
                campo_ordenacao = Medicamento.tarja
            elif ordenar_por == "fabricante":
                campo_ordenacao = Medicamento.fabricante
            elif ordenar_por == "criado_em":
                campo_ordenacao = Medicamento.criado_em
            
            if campo_ordenacao:
                if direcao == "desc":
                    query = query.order_by(desc(campo_ordenacao))
                else:
                    query = query.order_by(asc(campo_ordenacao))
        else:
            query = query.order_by(asc(Medicamento.nome))

        return query.offset(skip).limit(limit).all()

    def create(self, medicamento: MedicamentoCreate):
        db_medicamento = Medicamento(**medicamento.model_dump())
        self.db.add(db_medicamento)
        self.db.commit()
        self.db.refresh(db_medicamento)
        return db_medicamento

    def get_by_id(self, id_medicamento: int):
        # Atualizei aqui também para trazer os lotes ao ver detalhes de um único remédio
        return self.db.query(Medicamento).options(joinedload(Medicamento.lotes)).filter(Medicamento.id_medicamento == id_medicamento).first()
        
    def get_by_nome(self, nome: str):
        return self.db.query(Medicamento).filter(Medicamento.nome == nome).first()

    def update(self, db_medicamento: Medicamento, medicamento_update: MedicamentoUpdate):
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