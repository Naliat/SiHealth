# app/db/repositories/lote.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from app.models.lote import Lote
from app.models.medicamento import Medicamento
from app.schemas.lote import LoteCreate, LoteUpdate

class LoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        # Novos parâmetros de filtro
        numero_lote: str = None,
        nome_medicamento: str = None, # Filtro cruzado (filtra lote pelo nome do remédio)
        ordenar_por: str = None,
        direcao: str = "asc"
    ):
        # Inicia a query fazendo JOIN com Medicamento.
        # O joinedload garante que os dados do remédio venham no JSON de resposta.
        query = self.db.query(Lote).join(Medicamento).options(joinedload(Lote.medicamento))

        # --- FILTROS ---
        if numero_lote:
            query = query.filter(Lote.numero_lote.ilike(f"%{numero_lote}%"))
        
        if nome_medicamento:
            # Aqui filtramos a tabela Lote usando uma coluna da tabela Medicamento
            query = query.filter(Medicamento.nome.ilike(f"%{nome_medicamento}%"))

        # --- ORDENAÇÃO ---
        if ordenar_por:
            campo_ordenacao = None
            
            if ordenar_por == "numero_lote":
                campo_ordenacao = Lote.numero_lote
            elif ordenar_por == "validade": 
                campo_ordenacao = Lote.data_validade
            elif ordenar_por == "quantidade":
                campo_ordenacao = Lote.quantidade_atual
            elif ordenar_por == "medicamento": # Ordena A-Z pelo nome do remédio
                campo_ordenacao = Medicamento.nome
            elif ordenar_por == "criado_em":
                campo_ordenacao = Lote.criado_em
            
            if campo_ordenacao:
                if direcao == "desc":
                    query = query.order_by(desc(campo_ordenacao))
                else:
                    query = query.order_by(asc(campo_ordenacao))
        else:
            # Padrão: Ordenar por validade (vencimentos mais próximos primeiro)
            query = query.order_by(asc(Lote.data_validade))

        return query.offset(skip).limit(limit).all()

    # ... (Mantenha os outros métodos get_by_id, get_by_medicamento, create, update iguais) ...
    def get_by_id(self, id_lote: int):
        return self.db.query(Lote).options(joinedload(Lote.medicamento)).filter(Lote.id_lote == id_lote).first()

    def get_by_medicamento(self, id_medicamento: int):
        return self.db.query(Lote).options(joinedload(Lote.medicamento)).filter(Lote.id_medicamento == id_medicamento).all()

    def create(self, lote: LoteCreate):
        dados_lote = lote.model_dump()
        db_lote = Lote(**dados_lote, quantidade_atual=lote.quantidade_inicial)
        self.db.add(db_lote)
        self.db.commit()
        self.db.refresh(db_lote)
        # Retorna buscando pelo ID para garantir que o relacionamento 'medicamento' venha preenchido
        return self.get_by_id(db_lote.id_lote)

    def update(self, db_lote: Lote, lote_update: LoteUpdate):
        update_data = lote_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_lote, key, value)
        self.db.add(db_lote)
        self.db.commit()
        self.db.refresh(db_lote)
        return db_lote