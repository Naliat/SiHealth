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
        # Define o que é "Baixo Estoque" (Ex: menos de 20 unidades)
        self.limite_baixo_estoque = 20
        # Define o alerta de vencimento (Ex: vence nos próximos 30 dias)
        self.limite_vencimento = self.hoje + timedelta(days=30)

    def get_kpis(self):
        # 1. Itens com Baixo Estoque
        baixo_estoque = self.db.query(func.count(Lote.id_lote))\
            .filter(Lote.quantidade_atual < self.limite_baixo_estoque, Lote.quantidade_atual > 0).scalar()

        # 2. Itens Próximos do Vencimento (ou Vencidos)
        prox_vencimento = self.db.query(func.count(Lote.id_lote))\
            .filter(Lote.data_validade <= self.limite_vencimento, Lote.quantidade_atual > 0).scalar()

        # 3. Total de Itens em Estoque (Soma das quantidades)
        total_estoque = self.db.query(func.sum(Lote.quantidade_atual)).scalar() or 0

        # 4. Dispensações no Mês Atual
        mes_atual = self.hoje.month
        ano_atual = self.hoje.year
        dispensacoes = self.db.query(func.count(Saida.id_saida))\
            .filter(extract('month', Saida.data_saida) == mes_atual,\
                    extract('year', Saida.data_saida) == ano_atual).scalar()

        return {
            "itens_baixo_estoque": baixo_estoque,
            "itens_prox_vencimento": prox_vencimento,
            "total_itens_estoque": total_estoque,
            "dispensacoes_mensal": dispensacoes
        }

    def get_grafico_barras(self):
        # Top 5 Medicamentos mais retirados
        # Join: Saida -> Lote -> Medicamento
        resultados = self.db.query(
            Medicamento.nome,
            func.sum(Saida.quantidade_total_entregue).label("total")
        ).join(Lote, Saida.id_lote == Lote.id_lote)\
         .join(Medicamento, Lote.id_medicamento == Medicamento.id_medicamento)\
         .group_by(Medicamento.nome)\
         .order_by(desc("total"))\
         .limit(5).all()
        
        return [{"nome": r.nome, "total_saidas": r.total} for r in resultados]

    def get_grafico_linha(self):
        # Dispensações por mês (Últimos 12 meses seria o ideal, mas faremos simples por ano atual)
        ano_atual = self.hoje.year
        resultados = self.db.query(
            extract('month', Saida.data_saida).label("mes"),
            func.count(Saida.id_saida).label("qtd")
        ).filter(extract('year', Saida.data_saida) == ano_atual)\
         .group_by("mes")\
         .order_by("mes").all()

        # Formata para JSON (Meses numéricos 1, 2, 3...)
        return [{"mes": str(int(r.mes)), "quantidade": r.qtd} for r in resultados]

    def get_tabela_vencimento(self):
        # Lista os lotes que vencem em breve
        lotes = self.db.query(Lote).join(Medicamento)\
            .filter(Lote.data_validade <= self.limite_vencimento, Lote.quantidade_atual > 0)\
            .order_by(Lote.data_validade).limit(10).all()
        
        lista = []
        for l in lotes:
            status = "Vencido" if l.data_validade < self.hoje else "Próx. Venc."
            lista.append({
                "nome_medicamento": l.medicamento.nome,
                "numero_lote": l.numero_lote,
                "quantidade": l.quantidade_atual,
                "validade": l.data_validade,
                "status": status
            })
        return lista

    def get_tabela_baixo_estoque(self):
        lotes = self.db.query(Lote).join(Medicamento)\
            .filter(Lote.quantidade_atual < self.limite_baixo_estoque, Lote.quantidade_atual > 0)\
            .order_by(Lote.quantidade_atual).limit(10).all()
            
        return [{
            "nome_medicamento": l.medicamento.nome,
            "numero_lote": l.numero_lote,
            "quantidade": l.quantidade_atual,
            "validade": l.data_validade,
            "status": "Baixo Estoque"
        } for l in lotes]