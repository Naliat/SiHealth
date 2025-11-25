from sqlalchemy.orm import Session
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
        # Inicia a query base
        query = self.db.query(Medicamento)

        # --- FILTROS ---
        
        # 1. Filtro por Nome (Parcial)
        # Se digitar "dip", acha "Dipirona" e "Adipor"
        if nome_filtro:
            query = query.filter(Medicamento.nome.ilike(f"%{nome_filtro}%"))

        # 2. Filtro por Tarja (Exato ou Parcial)
        # Se digitar "Preta", traz só os de tarja preta
        if tarja_filtro:
            query = query.filter(Medicamento.tarja.ilike(f"%{tarja_filtro}%"))

        # --- ORDENAÇÃO ---
        
        if ordenar_por:
            campo_ordenacao = None
            
            # Mapeia a string da URL para a coluna do Banco
            if ordenar_por == "nome":
                campo_ordenacao = Medicamento.nome
            elif ordenar_por == "tarja":
                campo_ordenacao = Medicamento.tarja
            elif ordenar_por == "fabricante":
                campo_ordenacao = Medicamento.fabricante
            elif ordenar_por == "criado_em": # Útil para ver os últimos cadastrados
                campo_ordenacao = Medicamento.criado_em
            
            # Aplica a direção (Crescente ou Decrescente)
            if campo_ordenacao:
                if direcao == "desc":
                    query = query.order_by(desc(campo_ordenacao))
                else:
                    query = query.order_by(asc(campo_ordenacao))
        else:
            # Padrão: Ordenar por nome (A-Z) se o usuário não pedir nada
            query = query.order_by(asc(Medicamento.nome))

        return query.offset(skip).limit(limit).all()

    # ... Mantenha os métodos create, update, delete, get_by_id iguais ...
    def create(self, medicamento: MedicamentoCreate):
        db_medicamento = Medicamento(**medicamento.model_dump())
        self.db.add(db_medicamento)
        self.db.commit()
        self.db.refresh(db_medicamento)
        return db_medicamento

    def get_by_id(self, id_medicamento: int):
        return self.db.query(Medicamento).filter(Medicamento.id_medicamento == id_medicamento).first()
        
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