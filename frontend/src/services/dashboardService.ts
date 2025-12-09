export const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

export interface DashboardMetrics {
  lowStockItems: number
  nearExpiryItems: number
  totalStockItems: number
  monthlyDispensations: number
}

export interface DashboardTopMedication {
  nome: string
  quantidade: number
}

export interface DashboardDispensacaoPorMes {
  mes: string
  quantidade: number
}

export interface DashboardItemCritico {
  nome: string
  quantidade: number
  lote: string
  status: string
}

export interface DashboardResumo {
  metrics: DashboardMetrics
  topMedications: DashboardTopMedication[]
  dispensacoesPorMes: DashboardDispensacaoPorMes[]
  proximosAVencer: DashboardItemCritico[]
  baixaQuantidade: DashboardItemCritico[]
}

interface BackendDashboardKPIs {
  itens_baixo_estoque: number
  itens_prox_vencimento: number
  total_itens_estoque: number
  dispensacoes_mensal: number
}

interface BackendMedicamentoMaisRetirado {
  nome: string
  total_saidas: number
}

interface BackendFrequenciaMensal {
  mes: string
  quantidade: number
}

interface BackendItemAlerta {
  nome_medicamento: string
  numero_lote: string
  quantidade: number
  validade: string
  status: string
}

interface BackendDashboardResponse {
  kpis: BackendDashboardKPIs
  grafico_barras: BackendMedicamentoMaisRetirado[]
  grafico_linha: BackendFrequenciaMensal[]
  tabela_vencimento: BackendItemAlerta[]
  tabela_baixo_estoque: BackendItemAlerta[]
}

export async function getDashboardResumo (): Promise<DashboardResumo> {
  const res = await fetch(`${API_BASE_URL}/dashboard/`)

  if (!res.ok) {
    const errBody = await res.json().catch(() => null)
    const message = errBody?.detail || `HTTP ${res.status}`
    const error: any = new Error(message)
    error.status = res.status
    error.body = errBody
    throw error
  }

  const data = (await res.json()) as BackendDashboardResponse

  return {
    metrics: {
      lowStockItems: data.kpis.itens_baixo_estoque,
      nearExpiryItems: data.kpis.itens_prox_vencimento,
      totalStockItems: data.kpis.total_itens_estoque,
      monthlyDispensations: data.kpis.dispensacoes_mensal,
    },
    topMedications: data.grafico_barras.map(item => ({
      nome: item.nome,
      quantidade: item.total_saidas,
    })),
    dispensacoesPorMes: data.grafico_linha.map(item => ({
      mes: item.mes,
      quantidade: item.quantidade,
    })),
    proximosAVencer: data.tabela_vencimento.map(item => ({
      nome: item.nome_medicamento,
      quantidade: item.quantidade,
      lote: item.numero_lote,
      status: item.status,
    })),
    baixaQuantidade: data.tabela_baixo_estoque.map(item => ({
      nome: item.nome_medicamento,
      quantidade: item.quantidade,
      lote: item.numero_lote,
      status: item.status,
    })),
  }
}