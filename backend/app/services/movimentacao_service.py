from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.repositories import EntradaRepository, SaidaRepository, LoteRepository
from app.schemas.entrada import EntradaCreate
from app.schemas.saida import SaidaCreate

class MovimentacaoService:
    def __init__(self, db: Session):
        self.db = db
        self.entrada_repo = EntradaRepository(db)
        self.saida_repo = SaidaRepository(db)
        self.lote_repo = LoteRepository(db)

    def registrar_entrada(self, dados: EntradaCreate):
        # 1. Verifica se o lote existe
        lote = self.lote_repo.get_by_id(dados.id_lote)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote não encontrado")

        try:
            # 2. Cria o registro de entrada
            nova_entrada = self.entrada_repo.create(dados)
            
            # 3. ATUALIZA O ESTOQUE (Incrementa)
            lote.quantidade_atual += dados.quantidade
            
            # 4. Commit único (Atomicidade)
            self.db.commit()
            self.db.refresh(nova_entrada)
            return nova_entrada
        except Exception as e:
            self.db.rollback() # Desfaz tudo se der erro
            raise e

    def registrar_saida(self, dados: SaidaCreate):
        # 1. Verifica se o lote existe
        lote = self.lote_repo.get_by_id(dados.id_lote)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote não encontrado")

        # 2. Calcula o total sendo retirado
        quantidade_total = dados.numero_de_caixas_entregues * dados.quantidade_por_caixa

        # 3. VERIFICA SE TEM ESTOQUE SUFICIENTE
        if lote.quantidade_atual < quantidade_total:
            raise HTTPException(
                status_code=400, 
                detail=f"Estoque insuficiente. Disponível: {lote.quantidade_atual}, Solicitado: {quantidade_total}"
            )

        try:
            # 4. Cria registro de saída
            nova_saida = self.saida_repo.create(dados, quantidade_total)

            # 5. ATUALIZA O ESTOQUE (Decrementa)
            lote.quantidade_atual -= quantidade_total

            # 6. Commit
            self.db.commit()
            self.db.refresh(nova_saida)
            return nova_saida
        except Exception as e:
            self.db.rollback()
            raise e