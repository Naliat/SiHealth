# app/services/saida_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.repositories.saida import SaidaRepository
from app.models.lote import Lote
from app.models.saida import Saida
from app.schemas.saida import SaidaCreate

class SaidaService:
    def __init__(self, db: Session):
        self.db = db
        self.saida_repo = SaidaRepository(db)

    def registrar_saida(self, dados: SaidaCreate):
        # 1. BUSCAR LOTE PELO NÚMERO (STRING)
        # O usuário digitou "L2024-ABC", nós buscamos o ID real no banco
        lote = self.db.query(Lote).filter(Lote.numero_lote == dados.numero_lote).first()
        
        if not lote:
            raise HTTPException(
                status_code=404, 
                detail=f"Lote '{dados.numero_lote}' não encontrado no sistema."
            )

        # 2. VERIFICAR ESTOQUE
        if lote.quantidade_atual < dados.quantidade:
            raise HTTPException(
                status_code=400, 
                detail=f"Estoque insuficiente. O lote {lote.numero_lote} tem apenas {lote.quantidade_atual} unidades."
            )

        # 3. EFETUAR A BAIXA E SALVAR
        try:
            # Desconta do estoque
            lote.quantidade_atual -= dados.quantidade
            
            # Cria o registro de saída
            nova_saida = Saida(
                id_lote=lote.id_lote,
                cns_paciente=dados.cns_paciente,
                nome_paciente=dados.nome_paciente,
                quantidade=dados.quantidade,
                numero_receita=dados.numero_receita,
                tipo_saida=dados.tipo_saida,
                observacao=dados.observacao
            )
            
            self.saida_repo.create(nova_saida)
            self.db.commit()
            self.db.refresh(nova_saida)
            
            return nova_saida

        except Exception as e:
            self.db.rollback() # Desfaz a baixa de estoque se der erro ao salvar a saída
            raise e