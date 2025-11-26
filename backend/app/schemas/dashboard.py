from pydantic import BaseModel
from typing import List
from datetime import date

# 1. Cards do Topo (KPIs)
class DashboardKPIs(BaseModel):
    itens_baixo_estoque: int
    itens_prox_vencimento: int
    total_itens_estoque: int
    dispensacoes_mensal: int

# 2. Gráfico de Barras (Mais Retirados)
class MedicamentoMaisRetirado(BaseModel):
    nome: str
    total_saidas: int

# 3. Gráfico de Linha (Frequência Mensal)
class FrequenciaMensal(BaseModel):
    mes: str # Ex: "Jan", "Fev" ou "2024-01"
    quantidade: int

# 4. Tabelas de Alerta (Vencimento e Baixo Estoque)
class ItemAlerta(BaseModel):
    nome_medicamento: str
    numero_lote: str
    quantidade: int
    validade: date
    status: str # "Vencido", "Próx. Venc.", "Baixo Estoque"

# --- RESPOSTA COMPLETA ---
class DashboardResponse(BaseModel):
    kpis: DashboardKPIs
    grafico_barras: List[MedicamentoMaisRetirado]
    grafico_linha: List[FrequenciaMensal]
    tabela_vencimento: List[ItemAlerta]
    tabela_baixo_estoque: List[ItemAlerta]