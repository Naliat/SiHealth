# app/schemas/dashboard.py
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date

# 1. Cards do Topo (KPIs)
class DashboardKPIs(BaseModel):
    itens_baixo_estoque: int
    itens_prox_vencimento: int
    total_itens_estoque: int
    dispensacoes_mensal: int

# 2. Gráfico de Barras: Medicamentos mais retirados
class MedicamentoPopulares(BaseModel):
    nome: str
    total_saidas: int

# 3. Gráfico de Linha: Frequência de dispensações (Jan-Dez)
class FrequenciaMensal(BaseModel):
    mes: str # "1", "2", ... "12"
    quantidade: int

# 4. Tabelas de Alerta (Vencimento e Estoque Baixo)
class ItemAlerta(BaseModel):
    nome_medicamento: str
    lote: str
    quantidade: int
    data_validade: date
    status: str # "Vencido", "Próx. Venc.", "Baixo"

# --- RESPOSTA GERAL ---
class DashboardResponse(BaseModel):
    kpis: DashboardKPIs
    grafico_barras: List[MedicamentoPopulares]
    grafico_linha: List[FrequenciaMensal]
    tabela_vencimento: List[ItemAlerta]
    tabela_baixo_estoque: List[ItemAlerta]

    model_config = ConfigDict(from_attributes=True)