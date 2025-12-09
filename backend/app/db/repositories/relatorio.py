from sqlalchemy.orm import Session
from datetime import date, datetime, time
from app.models.saida import Saida
from app.models.lote import Lote
from app.models.medicamento import Medicamento

class RelatorioRepository:
    def __init__(self, db: Session):
        self.db = db

    # 1. Busca Movimentações (Histórico)
    def buscar_dispensacoes(self, data_inicio: date, data_fim: date):
        inicio = datetime.combine(data_inicio, time.min)
        fim = datetime.combine(data_fim, time.max)

        resultados = self.db.query(Saida)\
            .join(Lote, Saida.id_lote == Lote.id_lote)\
            .join(Medicamento, Lote.id_medicamento == Medicamento.id_medicamento)\
            .filter(Saida.data_saida >= inicio, Saida.data_saida <= fim)\
            .order_by(Saida.data_saida.desc())\
            .all()

        lista_formatada = []
        for s in resultados:
            item = {
                "data_hora": s.data_saida,
                "nome_medicamento": s.lote.medicamento.nome,
                "principio_ativo": s.lote.medicamento.principio_ativo,
                "fabricante": s.lote.fabricante,
                "lote": s.lote.numero_lote,
                "validade_lote": s.lote.data_validade,
                "quantidade_dispensada": s.quantidade,
                "cns_paciente": s.cns_paciente,
                "tipo_saida": s.tipo_saida
            }
            lista_formatada.append(item)
        return lista_formatada

    # 2. Busca Estoque Atual (Snapshot) - ESTA FUNÇÃO ESTAVA FALTANDO
    def buscar_estoque_total(self):
        # Traz Lote -> Medicamento, ordenado por Nome e depois Validade
        resultados = self.db.query(Lote)\
            .join(Medicamento)\
            .filter(Lote.quantidade_atual > 0)\
            .order_by(Medicamento.nome.asc(), Lote.data_validade.asc())\
            .all()
            
        lista_estoque = []
        for l in resultados:
            item = {
                "nome_medicamento": l.medicamento.nome,
                "principio_ativo": l.medicamento.principio_ativo,
                "tarja": l.medicamento.tarja,
                "lote": l.numero_lote,
                "fabricante": l.fabricante,
                "validade": l.data_validade,
                "quantidade_atual": l.quantidade_atual
            }
            lista_estoque.append(item)
        return lista_estoque