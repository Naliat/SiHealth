<template>
  <v-container class="page-container pa-10 bg-gradient" fluid>
    <div class="d-flex justify-space-between align-start mb-10 flex-wrap ga-6">
      <div>
        <h1 class="text-h3 font-weight-bold text-slate-900 mb-2">Dashboard</h1>
        <p class="text-h6 text-slate-600">Visão geral do estoque e dispensações</p>
      </div>
      <div class="d-flex align-center ga-4">
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
            <v-icon>mdi-cube-outline</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-label">Itens com Baixo Estoque</span>
            <span class="kpi-value">{{ metrics?.lowStockItems ?? 0 }}</span>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="kpi-card kpi-near-expiry" elevation="2" rounded="xl">
          <div class="kpi-icon">
            <v-icon>mdi-timer-sand</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-label">Itens Próx. Venc.</span>
            <span class="kpi-value">{{ metrics?.nearExpiryItems ?? 0 }}</span>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="kpi-card kpi-total-stock" elevation="2" rounded="xl">
          <div class="kpi-icon">
            <v-icon>mdi-archive-outline</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-label">Itens em Estoque</span>
            <span class="kpi-value">{{ metrics?.totalStockItems ?? 0 }}</span>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="kpi-card kpi-monthly-disp" elevation="2" rounded="xl">
          <div class="kpi-icon">
            <v-icon>mdi-check-circle-outline</v-icon>
          </div>
          <div class="kpi-content">
            <span class="kpi-label">Dispensações Mensais</span>
            <span class="kpi-value">{{ metrics?.monthlyDispensations ?? 0 }}</span>
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

          <div class="top-meds-list">
            <div
              v-for="med in topMedications"
              :key="med.nome"
              class="top-med-row d-flex align-center mb-3"
            >
              <div class="top-med-name">{{ med.nome }}</div>
              <div class="top-med-bar-wrapper">
                <div
                  class="top-med-bar"
                  :style="{ width: `${maxTopMedication > 0 ? (med.quantidade / maxTopMedication) * 100 : 0}%` }"
                />
              </div>
              <span class="top-med-value">{{ med.quantidade }}</span>
            </div>
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

          <div class="chart-placeholder">
            <svg class="chart-svg" viewBox="0 0 100 40">
              <polyline
                fill="none"
                :points="chartPoints"
                stroke="#22c55e"
                stroke-width="2"
              />
            </svg>
            <div class="chart-footer d-flex justify-space-between mt-2 text-caption text-slate-500">
              <span>Jan</span>
              <span>Fev</span>
              <span>Mar</span>
              <span>Abr</span>
              <span>Mai</span>
              <span>Jun</span>
              <span>Jul</span>
              <span>Ago</span>
              <span>Set</span>
              <span>Out</span>
              <span>Nov</span>
              <span>Dez</span>
            </div>
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
              <tr v-if="proximosAVencer.length === 0">
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
                </td>></tr>
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
              <tr v-if="baixaQuantidade.length === 0">
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

<script lang="ts" setup>
  import { computed, onMounted, ref } from 'vue'

  import {
    type DashboardDispensacaoPorMes,
    type DashboardItemCritico,
    type DashboardMetrics,
    type DashboardTopMedication,
    getDashboardResumo,
  } from '@/services/dashboardService'
  import { gerarRelatorioPDF } from '@/services/relatorioService'

  const loading = ref(true)
  const errorMessage = ref<string | null>(null)

  const metrics = ref<DashboardMetrics | null>(null)
  const topMedications = ref<DashboardTopMedication[]>([])
  const dispensacoesPorMes = ref<DashboardDispensacaoPorMes[]>([])
  const proximosAVencer = ref<DashboardItemCritico[]>([])
  const baixaQuantidade = ref<DashboardItemCritico[]>([])

  const maxTopMedication = computed(() => {
    if (topMedications.value.length === 0) return 0
    return Math.max(...topMedications.value.map(m => m.quantidade))
  })

  const chartPoints = computed(() => {
    if (dispensacoesPorMes.value.length === 0) return ''

    const maxQty = Math.max(...dispensacoesPorMes.value.map(item => item.quantidade), 1)

    return dispensacoesPorMes.value
      .map((p, idx, arr) => {
        const x = (idx / Math.max(arr.length - 1, 1)) * 100
        const y = 40 - (p.quantidade / maxQty) * 35
        return `${x},${y}`
      })
      .join(' ')
  })

  onMounted(async () => {
    try {
      const response = await getDashboardResumo()
      metrics.value = response.metrics
      topMedications.value = response.topMedications
      dispensacoesPorMes.value = response.dispensacoesPorMes
      proximosAVencer.value = response.proximosAVencer
      baixaQuantidade.value = response.baixaQuantidade
    } catch (error: any) {
      console.error('Erro ao carregar dashboard', error)
      errorMessage.value = 'Não foi possível carregar os dados do dashboard.'
    } finally {
      loading.value = false
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

  function handleGerarRelatorio (): void {
    if (!metrics.value) {
      errorMessage.value = 'Não há dados disponíveis para gerar o relatório.'
      return
    }

    try {
      gerarRelatorioPDF({
        metrics: metrics.value,
        topMedications: topMedications.value,
        dispensacoesPorMes: dispensacoesPorMes.value,
        proximosAVencer: proximosAVencer.value,
        baixaQuantidade: baixaQuantidade.value,
      })
    } catch (error: any) {
      console.error('Erro ao gerar relatório', error)
      errorMessage.value = 'Erro ao gerar o relatório. Tente novamente.'
    }
  }
</script>

<style scoped>
.bg-gradient {
  background: #e5edf5;
  min-height: 100vh;
}

.text-slate-900 {
  color: #0f172a;
}

.text-slate-600 {
  color: #475569;
}

.text-slate-500 {
  color: #64748b;
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
  font-size: 0.9rem;
  color: var(--slate-600);
}

.kpi-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--slate-900);
}

.kpi-low-stock {
  background: #fecaca;
}

.kpi-near-expiry {
  background: #fde68a;
}

.kpi-total-stock {
  background: #e5f0ff;
}

.kpi-monthly-disp {
  background: #bbf7d0;
}

.panel-card {
  padding: 20px 24px 24px;
  min-height: 100%;
  border-radius: 18px;
  border: 1px solid var(--slate-200);
  background: #f9fbff;
}

.panel-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--slate-900);
}

.panel-subtitle {
  font-size: 0.9rem;
  color: var(--slate-500);
}

.sort-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
  color: var(--slate-600) !important;
  border-color: var(--slate-300) !important;
}

.top-meds-list {
  margin-top: 8px;
}

.top-med-row {
  gap: 12px;
  display: flex;
  align-items: center;
}

.top-med-name {
  font-size: 0.9rem;
  color: var(--slate-900);
  min-width: 140px;
  max-width: 140px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.top-med-bar-wrapper {
  flex: 1;
  height: 8px;
  border-radius: 999px;
  background-color: #e5e7eb;
  overflow: hidden;
}

.top-med-bar {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #93c5fd, #22c55e);
  transition: width 0.3s ease;
}

.top-med-value {
  font-size: 0.75rem;
  color: var(--slate-500);
  min-width: 40px;
  text-align: right;
  font-weight: 600;
}

.chart-placeholder {
  margin-top: 4px;
}

.chart-svg {
  width: 100%;
  height: 190px;
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
}

.status-ok {
  background-color: #dcfce7 !important;
  color: #15803d !important;
}

.status-warning {
  background-color: #fef3c7 !important;
  color: #b45309 !important;
}

.status-expired {
  background-color: #fee2e2 !important;
  color: #b91c1c !important;
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
