# app/services/dashboard_service.py
from sqlalchemy.orm import Session
from app.db.repositories.dashboard import DashboardRepository

class DashboardService:
    def __init__(self, db: Session):
        self.repo = DashboardRepository(db)

    def obter_dados_dashboard(self):
        return {
            "kpis": self.repo.get_kpis(),
            "grafico_barras": self.repo.get_mais_retirados(),
            "grafico_linha": self.repo.get_frequencia_anual(),
            "tabela_vencimento": self.repo.get_tabela_vencimento(),
            "tabela_baixo_estoque": self.repo.get_tabela_baixo_estoque()
        }