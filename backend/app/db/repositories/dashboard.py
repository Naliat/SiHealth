# app/db/repositories/dashboard.py
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, desc
from datetime import date, timedelta
from app.models.lote import Lote
from app.models.medicamento import Medicamento
from app.models.saida import Saida

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db
        self.hoje = date.today()
        # Regras de Negócio (Você pode ajustar esses números)
        self.limite_baixo_estoque = 20
        self.dias_alerta_vencimento = 30

    def get_kpis(self):
        # 1. Contar lotes com baixo estoque (mas que não estão zerados)
        baixo = self.db.query(func.count(Lote.id_lote))\
            .filter(Lote.quantidade_atual < self.limite_baixo_estoque, Lote.quantidade_atual > 0).scalar()

        # 2. Contar lotes vencendo nos próximos 30 dias (ou já vencidos)
        data_limite = self.hoje + timedelta(days=self.dias_alerta_vencimento)
        vencendo = self.db.query(func.count(Lote.id_lote))\
            .filter(Lote.data_validade <= data_limite, Lote.quantidade_atual > 0).scalar()

        # 3. Total de caixas/unidades no estoque inteiro
        total = self.db.query(func.sum(Lote.quantidade_atual)).scalar() or 0

        # 4. Total de dispensações (saídas) neste mês atual
        mes_atual = self.hoje.month
        ano_atual = self.hoje.year
        dispensacoes = self.db.query(func.count(Saida.id_saida))\
            .filter(extract('month', Saida.data_saida) == mes_atual, 
                    extract('year', Saida.data_saida) == ano_atual).scalar() or 0

        return {
            "itens_baixo_estoque": baixo,
            "itens_prox_vencimento": vencendo,
            "total_itens_estoque": total,
            "dispensacoes_mensal": dispensacoes
        }

    def get_mais_retirados(self):
        # Top 5 medicamentos com mais saídas (Soma da quantidade retirada)
        # Join: Saida -> Lote -> Medicamento
        resultados = self.db.query(
            Medicamento.nome,
            func.sum(Saida.quantidade).label("total")
        ).join(Lote, Saida.id_lote == Lote.id_lote)\
         .join(Medicamento, Lote.id_medicamento == Medicamento.id_medicamento)\
         .group_by(Medicamento.nome)\
         .order_by(desc("total"))\
         .limit(5).all()
        
        return [{"nome": r.nome, "total_saidas": r.total} for r in resultados]

    def get_frequencia_anual(self):
        # Quantidade de saídas por mês no ano atual
        ano_atual = self.hoje.year
        resultados = self.db.query(
            extract('month', Saida.data_saida).label("mes"),
            func.count(Saida.id_saida).label("qtd")
        ).filter(extract('year', Saida.data_saida) == ano_atual)\
         .group_by("mes")\
         .order_by("mes").all()

        return [{"mes": str(int(r.mes)), "quantidade": r.qtd} for r in resultados]

    def get_tabela_vencimento(self):
        # Busca lotes vencidos ou a vencer, ordenados pela validade (mais urgentes primeiro)
        data_limite = self.hoje + timedelta(days=self.dias_alerta_vencimento)
        
        lotes = self.db.query(Lote).join(Medicamento)\
            .filter(Lote.data_validade <= data_limite, Lote.quantidade_atual > 0)\
            .order_by(Lote.data_validade).limit(5).all()
        
        lista_formatada = []
        for l in lotes:
            status = "Vencido" if l.data_validade < self.hoje else "Próx. Venc."
            lista_formatada.append({
                "nome_medicamento": l.medicamento.nome,
                "lote": l.numero_lote,
                "quantidade": l.quantidade_atual,
                "data_validade": l.data_validade,
                "status": status
            })
        return lista_formatada

    def get_tabela_baixo_estoque(self):
        # Busca lotes com pouco estoque
        lotes = self.db.query(Lote).join(Medicamento)\
            .filter(Lote.quantidade_atual < self.limite_baixo_estoque, Lote.quantidade_atual > 0)\
            .order_by(Lote.quantidade_atual).limit(5).all()
            
        return [{
            "nome_medicamento": l.medicamento.nome,
            "lote": l.numero_lote,
            "quantidade": l.quantidade_atual,
            "data_validade": l.data_validade,
            "status": "Baixo"
        } for l in lotes]