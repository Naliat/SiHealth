<script lang="ts" setup>
  import { computed, reactive, ref } from 'vue'
  import { useRouter } from 'vue-router'

  const API_BASE_URL = '/api/v1'

  const form = reactive({
    pacienteId: null as number | null,
    pacienteBusca: '',
    medicamentoId: null as number | null,
    loteId: null as number | null,
    numeroCaixas: 1,
    quantidadePorCaixa: 1,
    motivo: 'Dispensa ao Paciente',
    dataSaida: new Date().toISOString().slice(0, 10),
    observacao: '',
  })

  const state = ref({
    motivosSaida: [
      'Dispensa ao Paciente',
      'Devolução ao Fornecedor',
      'Descarte por Vencimento',
      'Descarte por Danificação',
      'Outros',
    ] as string[],
    pacientesItems: [] as any[],
    medicamentosItems: [] as any[],
    lotesDoMedicamento: [] as any[],
    loading: {
      pacientes: false,
      medicamentos: false,
      lotes: false,
      submit: false,
    },
    errors: {
      pacienteId: null as string | null,
      medicamentoId: null as string | null,
      loteId: null as string | null,
      numeroCaixas: null as string | null,
      quantidadePorCaixa: null as string | null,
    },
  })

  const router = useRouter()

  const loteSelecionado = computed(() => {
    if (!form.loteId) return null
    return state.value.lotesDoMedicamento.find((l: any) => l.id === form.loteId) || null
  })

  const quantidadeTotal = computed(() => {
    const n = Number(form.numeroCaixas) || 0
    const q = Number(form.quantidadePorCaixa) || 0
    return n * q
  })

  const lotesDisponiveis = computed(() => {
    return state.value.lotesDoMedicamento.map((l: any) => ({
      title: `Lote: ${l.codigo} - Val: ${formatDate(l.validade || l.data_validade)} (Estoque: ${l.quantidade_atual ?? l.estoque ?? 0})`,
      value: l.id,
      original: l,
    }))
  })

  function formatDate (dateString: string | null | undefined) {
    if (!dateString) return '-'
    const [year, month, day] = dateString.split('-')
    return `${day}/${month}/${year}`
  }

  function clearErrors () {
    for (const k of (Object.keys(state.value.errors) as Array<keyof typeof state.value.errors>)) {
      state.value.errors[k] = null
    }
  }

  async function fetchPacientes (search: string) {
    if (!search || search.length < 3) return
    state.value.loading.pacientes = true
    try {
      const params = new URLSearchParams({ search })
      const res = await fetch(`${API_BASE_URL}/pessoas?${params.toString()}`)
      if (!res.ok) {
        const errBody = await res.json().catch(() => null)
        console.error('Erro ao buscar pacientes', errBody)
        state.value.pacientesItems = []
        return
      }
      const data = await res.json()
      state.value.pacientesItems = Array.isArray(data) ? data : data.items ?? []
    } catch (error) {
      console.error(error)
      state.value.pacientesItems = []
    } finally {
      state.value.loading.pacientes = false
    }
  }

  async function fetchMedicamentos (search: string) {
    if (!search || search.length < 2) return
    state.value.loading.medicamentos = true
    try {
      const params = new URLSearchParams({ search })
      const res = await fetch(`${API_BASE_URL}/medicamento?${params.toString()}`)
      if (!res.ok) {
        const errBody = await res.json().catch(() => null)
        console.error('Erro ao buscar medicamentos', errBody)
        state.value.medicamentosItems = []
        return
      }
      const data = await res.json()
      state.value.medicamentosItems = Array.isArray(data) ? data : data.items ?? []
    } catch (error) {
      console.error(error)
      state.value.medicamentosItems = []
    } finally {
      state.value.loading.medicamentos = false
    }
  }

  async function fetchLotesPorMedicamento (medicamentoId: number | null) {
    if (!medicamentoId) {
      state.value.lotesDoMedicamento = []
      return
    }
    state.value.loading.lotes = true
    try {
      const params = new URLSearchParams({ medicamento_id: String(medicamentoId) })
      const res = await fetch(`${API_BASE_URL}/lote?${params.toString()}`)
      if (!res.ok) {
        const errBody = await res.json().catch(() => null)
        console.error('Erro ao buscar lotes', errBody)
        state.value.lotesDoMedicamento = []
        return
      }
      const data = await res.json()
      state.value.lotesDoMedicamento = Array.isArray(data) ? data : data.items ?? []
    } catch (error) {
      console.error(error)
      state.value.lotesDoMedicamento = []
    } finally {
      state.value.loading.lotes = false
    }
  }

  // OBS: Ajustar para pegar o ID real do usuário logado quando a store de auth estiver pronta.
  const idUsuarioResponsavel = 1

  // --- Validação ---
  function validateForm () {
    clearErrors()
    let valid = true

    if (!form.pacienteId) {
      state.value.errors.pacienteId = 'Selecione um paciente'
      valid = false
    }
    if (!form.medicamentoId) {
      state.value.errors.medicamentoId = 'Selecione um medicamento'
      valid = false
    }
    if (!form.loteId) {
      state.value.errors.loteId = 'Selecione um lote'
      valid = false
    }
    if (!form.numeroCaixas || form.numeroCaixas < 1) {
      state.value.errors.numeroCaixas = 'Informe o número de caixas (>= 1)'
      valid = false
    }
    if (!form.quantidadePorCaixa || form.quantidadePorCaixa < 1) {
      state.value.errors.quantidadePorCaixa = 'Informe a quantidade por caixa (>= 1)'
      valid = false
    }

    const lote = loteSelecionado.value
    if (lote) {
      const estoque = lote.quantidade_atual ?? lote.estoque ?? 0
      if (quantidadeTotal.value > estoque) {
        state.value.errors.numeroCaixas = `Estoque insuficiente. Disponível: ${estoque}, solicitado: ${quantidadeTotal.value}`
        valid = false
      }
    }

    return valid
  }

  async function submitForm () {
    if (!validateForm()) return

    state.value.loading.submit = true
    try {
      const payload = {
        numero_de_caixas_entregues: Number(form.numeroCaixas),
        quantidade_por_caixa: Number(form.quantidadePorCaixa),
        observacao: form.observacao?.trim() || '',
        id_lote: Number(form.loteId),
        id_paciente: Number(form.pacienteId),
        id_usuario_responsavel: Number(idUsuarioResponsavel),
      }

      const res = await fetch(`${API_BASE_URL}/movimentacao/saida`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}))
        console.error('Erro ao registrar saída', errBody)
        return
      }

      resetForm()
      console.log('Saída registrada com sucesso')
    } catch (error) {
      console.error(error)
    } finally {
      state.value.loading.submit = false
    }
  }

  function resetForm () {
    form.pacienteId = null
    form.pacienteBusca = ''
    form.medicamentoId = null
    form.loteId = null
    form.numeroCaixas = 1
    form.quantidadePorCaixa = 1
    form.motivo = 'Dispensa ao Paciente'
    form.dataSaida = new Date().toISOString().slice(0, 10)
    form.observacao = ''
    state.value.pacientesItems = []
    state.value.medicamentosItems = []
    state.value.lotesDoMedicamento = []
    clearErrors()
  }

  function onMedicamentoChange (value: number | null) {
    form.medicamentoId = value
    form.loteId = null
    form.numeroCaixas = 1
    form.quantidadePorCaixa = 1
    fetchLotesPorMedicamento(value)
  }

  function onPacienteSearch (search: string) {
    form.pacienteBusca = search
    fetchPacientes(search)
  }

  function onMedicamentoSearch (search: string) {
    fetchMedicamentos(search)
  }
</script>

<template>
  <v-container class="page-container pa-8 bg-gradient" fluid>
    <div class="d-flex justify-space-between align-start mb-8">
      <div>
        <h1 class="text-h3 font-weight-bold text-slate-900 mb-2">Registrar Saída</h1>
        <p class="text-h6 text-slate-600">Registro de saídas do estoque</p>
      </div>

      <v-btn class="user-btn" variant="text">
        <v-icon start>mdi-account-circle</v-icon>
        Usuário
        <v-icon end size="small">mdi-chevron-down</v-icon>
      </v-btn>
    </div>

    <v-form @submit.prevent="submitForm">
      <!-- Dados do Paciente -->
      <v-card class="section-card mb-6" elevation="1" rounded="xl">
        <div class="section-body">
          <h2 class="section-title">Dados do Paciente:</h2>

          <v-row dense>
            <v-col cols="12">
              <label class="input-label">CNS:</label>
              <v-autocomplete
                v-model="form.pacienteId"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details="auto"
                item-title="nome"
                item-value="id"
                :items="state.pacientesItems"
                :loading="state.loading.pacientes"
                placeholder="Digite ao menos 3 caracteres para buscar..."
                variant="solo"
                @update:search="onPacienteSearch"
              />
              <div v-if="state.errors.pacienteId" class="error-text">{{ state.errors.pacienteId }}</div>
            </v-col>

            <v-col cols="12">
              <label class="input-label">Nome do paciente:</label>
              <v-text-field
                bg-color="#f1f5f9"
                class="rounded-input"
                disabled
                flat
                hide-details
                placeholder="Preenchido automaticamente ao selecionar o CNS"
                variant="solo"
              />
            </v-col>

            <v-col cols="12">
              <label class="input-label">Número da receita (opcional):</label>
              <v-text-field
                bg-color="#f1f5f9"
                class="rounded-input"
                disabled
                flat
                hide-details
                placeholder="Campo ainda não integrado"
                variant="solo"
              />
            </v-col>
          </v-row>
        </div>
      </v-card>

      <!-- Informações do Remédio -->
      <v-card class="section-card mb-6" elevation="1" rounded="xl">
        <div class="section-body">
          <h2 class="section-title">Informações do Remédio:</h2>

          <v-row dense>
            <v-col cols="12">
              <label class="input-label d-flex justify-space-between align-center">
                <span>Lote:</span>
                <span v-if="loteSelecionado" class="text-caption text-slate-500">
                  Val: {{ formatDate(loteSelecionado.validade || loteSelecionado.data_validade) }}
                </span>
              </label>
              <v-select
                v-model="form.loteId"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details="auto"
                :items="lotesDisponiveis"
                :loading="state.loading.lotes"
                no-data-text="Nenhum lote disponível para este medicamento"
                placeholder="Selecione o lote"
                variant="solo"
              />
              <div v-if="state.errors.loteId" class="error-text">{{ state.errors.loteId }}</div>
            </v-col>
          </v-row>

          <v-row dense>
            <v-col cols="12">
              <label class="input-label">Nome do remédio:</label>
              <v-autocomplete
                v-model="form.medicamentoId"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details="auto"
                item-title="nome"
                item-value="id"
                :items="state.medicamentosItems"
                :loading="state.loading.medicamentos"
                placeholder="Digite para buscar o medicamento..."
                variant="solo"
                @update:model-value="onMedicamentoChange"
                @update:search="onMedicamentoSearch"
              >
                <template #append-inner>
                  <v-icon class="mr-1 text-slate-500" size="small">mdi-magnify</v-icon>
                </template>
              </v-autocomplete>
              <div v-if="state.errors.medicamentoId" class="error-text">{{ state.errors.medicamentoId }}</div>
            </v-col>
          </v-row>

          <v-row dense>
            <v-col cols="12">
              <div class="d-flex justify-space-between align-center">
                <label class="input-label mb-0">Caixas:</label>
                <div class="stepper-wrapper">
                  <div class="custom-stepper" :class="{ 'stepper-disabled': !form.loteId }">
                    <v-btn
                      :disabled="!form.loteId || form.numeroCaixas <= 1"
                      icon
                      size="x-small"
                      variant="text"
                      @click="form.numeroCaixas > 1 && (form.numeroCaixas -= 1)"
                    >
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>

                    <input
                      v-model.number="form.numeroCaixas"
                      class="stepper-input"
                      :disabled="!form.loteId"
                      min="1"
                      type="number"
                    >

                    <v-btn
                      :disabled="!form.loteId"
                      icon
                      size="x-small"
                      variant="text"
                      @click="form.numeroCaixas += 1"
                    >
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                  </div>
                </div>
              </div>
              <div v-if="state.errors.numeroCaixas" class="error-text">{{ state.errors.numeroCaixas }}</div>
            </v-col>
          </v-row>

          <!-- Linha: Quantidade por caixa + Total -->
          <v-row dense>
            <v-col cols="12" md="6">
              <label class="input-label">Quantidade por caixa:</label>
              <v-text-field
                v-model.number="form.quantidadePorCaixa"
                bg-color="#f1f5f9"
                class="rounded-input"
                :disabled="!form.loteId"
                flat
                hide-details
                min="1"
                placeholder="Ex: 30"
                type="number"
                variant="solo"
              />
              <div v-if="state.errors.quantidadePorCaixa" class="error-text">{{ state.errors.quantidadePorCaixa }}</div>
            </v-col>

            <v-col class="d-flex align-center" cols="12" md="6">
              <div
                class="info-box w-100"
                :class="{ 'info-box-error': state.errors.numeroCaixas || state.errors.quantidadePorCaixa }"
              >
                <span class="text-caption text-slate-500">Total a retirar</span>
                <div class="text-body-1 font-weight-bold text-slate-900">
                  {{ quantidadeTotal }} unidades
                </div>
                <div v-if="loteSelecionado" class="text-caption text-slate-500 mt-1">
                  Disponível:
                  <span class="font-weight-medium">
                    {{ loteSelecionado.quantidade_atual ?? loteSelecionado.estoque ?? 0 }} unidades
                  </span>
                </div>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-card>

      <!-- Finalização -->
      <v-card class="section-card mb-6" elevation="1" rounded="xl">
        <div class="section-body">
          <h2 class="section-title">Finalização:</h2>

          <v-row dense>
            <v-col cols="12">
              <label class="input-label">Tipo de saída:</label>
              <v-select
                v-model="form.motivo"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details
                :items="state.motivosSaida"
                variant="solo"
              />
            </v-col>
          </v-row>
        </div>
      </v-card>

      <div class="form-actions d-flex justify-end align-center">
        <v-btn
          class="text-slate-600"
          rounded="lg"
          size="large"
          variant="text"
          @click="router.back()"
        >
          Cancelar
        </v-btn>
        <v-btn
          class="concluir-btn px-10"
          color="primary"
          :disabled="state.loading.submit"
          :loading="state.loading.submit"
          rounded="lg"
          size="large"
          type="submit"
        >
          Concluir
        </v-btn>
      </div>
    </v-form>
  </v-container>
</template>

<style scoped>
.bg-gradient {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
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

.section-card {
  padding: 24px;
  background-color: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.section-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
}

.user-btn {
  color: #475569 !important;
  text-transform: none;
  letter-spacing: normal;
}

.input-label {
  display: block;
  font-weight: 600;
  font-size: 0.875rem;
  color: #0f172a;
  margin-bottom: 4px;
}

.input-label.mb-0 {
  margin-bottom: 0;
}

.rounded-input :deep(.v-field) {
  border-radius: 10px !important;
  border: 1px solid #e2e8f0;
  box-shadow: none;
}

.info-box {
  background-color: #f8fafc;
  padding: 12px 16px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.info-box-error {
  border-color: #fecaca;
  background-color: #fef2f2;
}

.stepper-wrapper {
  display: flex;
  align-items: center;
}

.custom-stepper {
  display: inline-flex;
  align-items: center;
  background-color: #f8fafc;
  border-radius: 999px;
  padding: 4px 8px;
  height: 40px;
  border: 1px solid #e2e8f0;
}

.stepper-disabled {
  opacity: 0.5;
}

.custom-stepper :deep(.v-btn) {
  min-width: 24px;
  color: #64748b;
}

.stepper-input {
  width: 48px;
  text-align: center;
  font-weight: 600;
  color: #475569;
  border: none;
  outline: none;
  background: transparent;
  -moz-appearance: textfield;
}

.stepper-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}

.concluir-btn {
  font-weight: 600;
  text-transform: none;
  box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.15);
}

.error-text {
  color: #b91c1c;
  font-size: 0.75rem;
  margin-top: 4px;
}

.form-actions {
  gap: 12px;
  margin-top: 8px;
}
</style>
