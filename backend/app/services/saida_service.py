from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.repositories.saida import SaidaRepository
from app.db.repositories.lote import LoteRepository
from app.schemas.saida import SaidaCreate

class SaidaService:
    def __init__(self, db: Session):
        self.db = db
        self.saida_repo = SaidaRepository(db)
        self.lote_repo = LoteRepository(db)

    def registrar_saida(self, dados: SaidaCreate):
        # 1. Busca Lote
        lote = self.lote_repo.get_by_id(dados.id_lote)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote não encontrado")

        # 2. Calcula Total (Caixas * Unidades)
        quantidade_total = dados.numero_de_caixas * dados.quantidade_por_caixa

        # 3. Valida Estoque
        if lote.quantidade_atual < quantidade_total:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Estoque insuficiente. Disponível: {lote.quantidade_atual} unidades"
            )

        try:
            # 4. Baixa no Estoque
            lote.quantidade_atual -= quantidade_total

            # 5. Salva Registro
            nova_saida = self.saida_repo.create(dados, quantidade_total)
            
            self.db.commit()
            self.db.refresh(nova_saida)
            return nova_saida

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))