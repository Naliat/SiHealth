<script lang="ts" setup>
import { computed, ref, onMounted } from 'vue'
import { format } from 'date-fns'

import { 
    getDashboardResumo 
} from '@/services/dashboardService' 
import { 
    baixarRelatorioGeral
} from '@/services/relatorioService' 

import type { 
    DashboardMetrics, 
    DashboardTopMedication, 
    DashboardDispensacaoPorMes,
    DashboardItemCritico
} from '@/services/dashboardService' 

import BarChart from '@/components/BarChart.vue' 
import LineChart from '@/components/LineChart.vue'

const loading = ref(true)
const errorMessage = ref<string | null>(null)

const metrics = ref<DashboardMetrics | null>(null)
const topMedications = ref<DashboardTopMedication[]>([])
const dispensacoesPorMes = ref<DashboardDispensacaoPorMes[]>([])
const proximosAVencer = ref<DashboardItemCritico[]>([])
const baixaQuantidade = ref<DashboardItemCritico[]>([])

const barChartData = computed(() => {
    return topMedications.value.map(item => ({
        label: item.nome,
        value: (
            typeof item.quantidade === 'number' && !isNaN(item.quantidade) ? item.quantidade : 0
        )
    }))
})

const lineChartData = computed(() => {
    const dataValues = dispensacoesPorMes.value.map(item => (
        typeof item.quantidade === 'number' && !isNaN(item.quantidade) ? item.quantidade : 0
    ));

    return {
        labels: dispensacoesPorMes.value.map(item => item.mes),
        datasets: [{
            data: dataValues,
            label: "Dispensações" 
        }]
    }
})


function getStatusChipClass (status: string): string {
  switch (status) {
    case 'Vencido': {
      return 'status-chip status-expired'
    }
    case 'Próx. Venc.': {
      return 'status-chip status-warning'
    }
    default: {
      return 'status-chip status-ok'
    }
  }
}
async function handleGerarRelatorio (): Promise<void> {
    if (loading.value) return; 

    const hoje = new Date();
    const trintaDiasAtras = new Date(hoje.setDate(hoje.getDate() - 30));
    
    const dataInicio = format(trintaDiasAtras, 'yyyy-MM-dd');
    const dataFim = format(new Date(), 'yyyy-MM-dd');

    try {
      errorMessage.value = null;
      console.log(`Solicitando relatório geral de ${dataInicio} até ${dataFim}...`);
      
      await baixarRelatorioGeral(dataInicio, dataFim);
      
      errorMessage.value = `Relatório PDF de ${dataInicio} a ${dataFim} gerado com sucesso!`;

    } catch (error: any) {
      console.error('Erro ao gerar relatório FastAPI', error);
      errorMessage.value = `Falha ao gerar o relatório. Status: ${error.status || 'Erro de rede'}.`;
    }
  }


onMounted(async () => {
  try {
    const response = await getDashboardResumo()
    
    console.log('Resposta do Dashboard (Inspeção):', response) 
    
    metrics.value = response.metrics
    topMedications.value = response.topMedications
    dispensacoesPorMes.value = response.dispensacoesPorMes
    proximosAVencer.value = response.proximosAVencer
    baixaQuantidade.value = response.baixaQuantidade
  } catch (error: any) {
    console.error('Erro ao carregar dashboard', error)
    errorMessage.value = `Erro de Conexão. Não foi possível carregar os dados. Verifique se o servidor está ativo. Detalhe: ${error.message || 'Erro de rede.'}`
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <v-container class="page-container pa-10 bg-gradient" fluid>
    <div class="d-flex justify-space-between align-start mb-10 flex-wrap ga-6">
      <div>
        <h1 class="text-h3 font-weight-bold text-slate-900 mb-2">Dashboard</h1>
        <p class="text-h6 text-slate-600">Visão geral do estoque e dispensações</p>
      </div>
      <div class="d-flex justify-space-between align-center ga-4">
        <v-btn
          class="report-btn"
          color="primary"
          :disabled="loading || !metrics"
          height="44"
          rounded="xl"
          variant="flat"
          @click="handleGerarRelatorio"
        >
          <v-icon start>mdi-file-chart</v-icon>
          Gerar relatório
        </v-btn>
        <v-btn class="user-btn" height="44" rounded="xl" variant="elevated">
          <v-icon start>mdi-account-circle-outline</v-icon>
          Usuário
          <v-icon end size="small">mdi-chevron-down</v-icon>
        </v-btn>
      </div>
    </div>

    <v-alert
      v-if="errorMessage"
      class="mb-6"
      density="comfortable"
      type="warning"
      variant="tonal"
    >
      {{ errorMessage }}
    </v-alert>

    <v-progress-linear
      v-if="loading"
      class="mb-4"
      color="primary"
      indeterminate
      rounded
    />

    <v-row class="mb-6" dense>
      <v-col cols="12" md="3" sm="6">
        <v-card class="kpi-card kpi-low-stock" elevation="2" rounded="xl">
          <div class="kpi-icon">
            <v-icon size="24">mdi-cube-send</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-value text-red-darken-3">{{ metrics?.lowStockItems ?? 0 }}</span>
            <span class="kpi-label text-red-darken-3">Itens com Baixo Estoque</span>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="kpi-card kpi-near-expiry" elevation="2" rounded="xl">
          <div class="kpi-icon">
            <v-icon size="24">mdi-timer-sand</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-value text-amber-darken-3">{{ metrics?.nearExpiryItems ?? 0 }}</span>
            <span class="kpi-label text-amber-darken-3">Itens Próx. Venc.</span>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="kpi-card kpi-total-stock" elevation="2" rounded="xl">
          <div class="kpi-icon">
            <v-icon size="24">mdi-archive-outline</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-value text-blue-darken-3">{{ metrics?.totalStockItems ?? 0 }}</span>
            <span class="kpi-label text-blue-darken-3">Itens em Estoque</span>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="kpi-card kpi-monthly-disp" elevation="2" rounded="xl">
          <div class="kpi-icon">
            <v-icon size="24">mdi-pill</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-value text-green-darken-3">{{ metrics?.monthlyDispensations ?? 0 }}</span>
            <span class="kpi-label text-green-darken-3">Dispensações Mensais</span>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mb-6" dense>
      <v-col cols="12" md="6">
        <v-card class="panel-card" elevation="2" rounded="xl">
          <div class="panel-header d-flex justify-space-between align-center mb-4">
            <div>
              <h2 class="panel-title">Medicamentos mais retirados</h2>
              <p class="panel-subtitle">Ranking dos itens mais dispensados</p>
            </div>
            <div class="d-flex align-center ga-2 text-slate-600 text-body-2">
              <span>sort:</span>
              <v-btn class="sort-btn" size="small" variant="outlined">
                Alfabética
                <v-icon end size="18">mdi-chevron-down</v-icon>
              </v-btn>
            </div>
          </div>

          <div v-if="loading" class="text-center text-slate-500">Carregando dados...</div>
          <div v-else-if="barChartData.length === 0" class="text-center text-slate-500">Nenhum dado de retirada disponível.</div>
          <div 
            v-else 
            :style="{ height: '250px', overflowY: 'auto', paddingRight: '10px' }"
          >
             <BarChart :data="barChartData" />
          </div>
          </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="panel-card" elevation="2" rounded="xl">
          <div class="panel-header d-flex justify-space-between align-center mb-4">
            <div>
              <h2 class="panel-title">Freq. de dispensações</h2>
              <p class="panel-subtitle">Resumo por mês</p>
            </div>
            <div class="d-flex align-center ga-2 text-slate-600 text-body-2">
              <span>sort:</span>
              <v-btn class="sort-btn" size="small" variant="outlined">
                2025
                <v-icon end size="18">mdi-chevron-down</v-icon>
              </v-btn>
            </div>
          </div>

          <div v-if="loading" class="text-center text-slate-500">Carregando dados...</div>
          <div v-else-if="lineChartData.datasets[0].data.length === 0" class="chart-wrapper text-center text-slate-500">Dados de frequência indisponíveis.</div>
          <div v-else class="chart-wrapper">
             <LineChart 
                :data="lineChartData.datasets" 
                :labels="lineChartData.labels" 
             />
          </div>
          </v-card>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col cols="12" md="6">
        <v-card class="panel-card" elevation="2" rounded="xl">
          <div class="panel-header mb-4">
            <h2 class="panel-title">Itens próx. de venc.</h2>
          </div>
          <v-table class="compact-table">
            <thead>
              <tr>
                <th class="text-left">Tt Nome do remédio</th>
                <th class="text-center" style="width: 80px">Quantidade</th>
                <th class="text-center" style="width: 120px"># Lote</th>
                <th class="text-center" style="width: 120px">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="proximosAVencer.length === 0 && !loading">
                <td class="text-center text-slate-500" colspan="4">
                  Nenhum item próximo do vencimento.
                </td>
              </tr>
              <tr
                v-for="item in proximosAVencer"
                v-else
                :key="item.lote + item.nome + item.status"
              >
                <td>{{ item.nome }}</td>
                <td class="text-center">{{ item.quantidade }}</td>
                <td class="text-center">{{ item.lote }}</td>
                <td class="text-center">
                  <v-chip :class="getStatusChipClass(item.status)" size="small">
                    {{ item.status }}
                  </v-chip>
                </td></tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="panel-card" elevation="2" rounded="xl">
          <div class="panel-header mb-4">
            <h2 class="panel-title">Itens com baixa quantidade</h2>
          </div>
          <v-table class="compact-table">
            <thead>
              <tr>
                <th class="text-left">Tt Nome do remédio</th>
                <th class="text-center" style="width: 80px">Quantidade</th>
                <th class="text-center" style="width: 120px"># Lote</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="baixaQuantidade.length === 0 && !loading">
                <td class="text-center text-slate-500" colspan="3">
                  Nenhum item com baixa quantidade.
                </td>
              </tr>
              <tr
                v-for="item in baixaQuantidade"
                v-else
                :key="item.lote + item.nome + item.quantidade"
              >
                <td>
                  <div class="d-flex align-center ga-2">
                    <span class="dot dot-red" />
                    <span>{{ item.nome }}</span>
                  </div>
                </td>
                <td class="text-center">{{ item.quantidade }}</td>
                <td class="text-center">{{ item.lote }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.bg-gradient {
  background: #e5edf5;
  min-height: 100vh;
}

.text-slate-900 {
  color: #1a202c;
}

.text-slate-600 {
  color: #4a5568;
}

.text-slate-500 {
  color: #718096;
}

.user-btn {
  text-transform: none;
  letter-spacing: normal;
  color: var(--slate-600) !important;
  background: #e5edf5 !important;
}

.user-btn .v-icon {
  color: var(--slate-600);
}

.report-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
  font-weight: 600;
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 22px;
  border-radius: 18px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  box-shadow: var(--shadow-sm);
}

.kpi-icon {
  width: 44px;
  height: 44px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1f2937;
  background-color: rgba(255, 255, 255, 0.6);
}

.kpi-content {
  display: flex;
  flex-direction: column;
}

.kpi-label {
  font-size: 0.85rem;
  font-weight: 500;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 800;
}

.kpi-low-stock {
  background: #fef2f2;
}

.kpi-near-expiry {
  background: #fefce8;
}

.kpi-total-stock {
  background: #ebf4ff;
}

.kpi-monthly-disp {
  background: #d1fae5;
}

.panel-card {
  padding: 20px 24px 24px;
  min-height: 100%;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
}

.panel-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a202c;
}

.panel-subtitle {
  font-size: 0.9rem;
  color: #718096;
  margin-top: -2px;
}

.sort-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
  color: var(--slate-600) !important;
  border-color: var(--slate-300) !important;
}

.chart-wrapper {
    position: relative;
    height: 250px; 
}


.compact-table {
  border-radius: 18px;
  overflow: hidden;
  background: #f9fbff;
}

.compact-table thead tr {
  background-color: #edf2ff;
}

.compact-table th {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6b7280;
  padding: 8px 12px;
}

.compact-table td {
  font-size: 0.85rem;
  color: #111827;
  padding: 10px 12px;
  border-top: 1px solid #e5e7eb;
}

.status-chip {
  font-size: 0.75rem;
  font-weight: 500;
  height: 24px;
}

.status-expired {
  background-color: #fee2e2 !important;
  color: #b91c1c !important;
}

.status-warning {
  background-color: #fef3c7 !important;
  color: #b45309 !important;
}

.status-ok {
  background-color: #dcfce7 !important;
  color: #15803d !important;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.dot-red {
  background-color: #ef4444;
}

@media (max-width: 960px) {
  .kpi-card {
    margin-bottom: 8px;
  }
}
</style>