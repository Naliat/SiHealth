<script lang="ts" setup>
  import { computed, reactive, ref, watch } from 'vue'
  import { useRouter } from 'vue-router'

  const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
  const API_TIMEOUT = 5000
  const SYSTEM_SECRET_PASSWORD = import.meta.env.VITE_MASTER_PASSWORD || 'admin_ubs_2025'

  interface LoteDetalhe {
    numero_lote: string
    quantidade_por_caixa: number
    quantidade_atual: number
    data_validade: string
    numero_caixa: string
    id_lote: number
    medicamento: { nome: string, id_medicamento: number }
  }

  const form = reactive({
    cnsPaciente: null as string | null,
    pacienteBusca: '',
    nomePacienteSnapshot: null as string | null,
    numeroReceita: null as string | null,

    medicamentoId: null as number | null,
    loteId: null as number | null,

    nomeRemedioManual: null as string | null,

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
    medicamentosItems: [] as any[],
    lotesDisponiveisBusca: [] as LoteDetalhe[],
    loteDetalhado: null as LoteDetalhe | null,
    loading: {
      medicamentos: false,
      lotes: false,
      submit: false,
    },
    errors: {
      cnsPaciente: null as string | null,
      medicamentoId: null as string | null,
      loteId: null as string | null,
      numeroCaixas: null as string | null,
      quantidadePorCaixa: null as string | null,
    },
  })

  const showConfirmPasswordDialog = ref(false)
  const masterPassword = ref('')
  const masterPasswordError = ref(false)
  const showSnackbar = ref(false)
  const snackbarMessage = ref('')
  const snackbarColor = ref('success')

  const router = useRouter()

  const quantidadeTotal = computed(() => {
    const n = Number(form.numeroCaixas) || 0
    const q = Number(form.quantidadePorCaixa) || 0
    return n * q
  })

  const loteSelecionado = computed(() => {
    if (!form.loteId) return null
    return state.value.lotesDisponiveisBusca.find(l => l.id_lote === form.loteId) || state.value.loteDetalhado
  })

  const lotesFormatados = computed(() => {
    return state.value.lotesDisponiveisBusca.map(l => ({
      title: `Lote: ${l.numero_lote} | Validade: ${formatDate(l.data_validade)} | Disponível: ${l.quantidade_atual ?? 0} unidades`,
      value: l.id_lote,
      original: l,
    }))
  })

  function formatDate (dateString: string | null | undefined) {
    if (!dateString) return '-'
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${day}/${month}/${year}`
  }

  function clearErrors () {
    for (const k of (Object.keys(state.value.errors) as Array<keyof typeof state.value.errors>)) {
      state.value.errors[k] = null
    }
  }

  let medicamentoSearchTimeout: ReturnType<typeof setTimeout>

  async function searchMedicamentos (query: string) {
    const q = query.trim()

    clearTimeout(medicamentoSearchTimeout)

    if (q.length === 0 && query !== '') {
      state.value.medicamentosItems = []
      return
    }

    const delay = q.length >= 2 || q.length === 0 ? 300 : 0

    medicamentoSearchTimeout = setTimeout(async () => {
      state.value.loading.medicamentos = true
      try {
        const params = new URLSearchParams()

        if (q) {
          params.append('nome', q)
        }
        params.append('limit', '20')

        const res = await fetch(`${API_BASE_URL}/medicamentos?${params.toString()}`)

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
    }, delay)
  }

  function handleOpenMedicamentoAutocomplete () {
    if (state.value.medicamentosItems.length === 0) {
      searchMedicamentos('')
    }
  }

  let loteSearchTimeout: ReturnType<typeof setTimeout>

  async function searchLotes (query: string) {
    const q = query.trim()

    clearTimeout(loteSearchTimeout)

    if (!form.medicamentoId) {
      state.value.lotesDisponiveisBusca = []
      return
    }

    if (q.length === 0 && query !== '') {
      state.value.lotesDisponiveisBusca = []
      return
    }

    const delay = q.length >= 2 || q.length === 0 ? 300 : 0

    loteSearchTimeout = setTimeout(async () => {
      state.value.loading.lotes = true
      try {
        const params = new URLSearchParams()

        params.append('id_medicamento', String(form.medicamentoId))

        if (q) {
          params.append('numero_lote', q)
        }
        params.append('limit', '20')

        const res = await fetch(`${API_BASE_URL}/lotes?${params.toString()}`)

        if (!res.ok) {
          const errBody = await res.json().catch(() => null)
          console.error('Erro ao buscar lotes', errBody)
          state.value.lotesDisponiveisBusca = []
          return
        }

        const data = await res.json()
        const lotes = Array.isArray(data) ? data : data.items ?? []

        state.value.lotesDisponiveisBusca = lotes
          .filter((l: LoteDetalhe) => l.medicamento?.id_medicamento === form.medicamentoId)
          .toSorted((a: LoteDetalhe, b: LoteDetalhe) => {
            const dateA = new Date(a.data_validade).getTime()
            const dateB = new Date(b.data_validade).getTime()
            return dateA - dateB
          })
      } catch (error) {
        console.error(error)
        state.value.lotesDisponiveisBusca = []
      } finally {
        state.value.loading.lotes = false
      }
    }, delay)
  }

  function handleOpenLoteAutocomplete () {
    if (form.medicamentoId && state.value.lotesDisponiveisBusca.length === 0) {
      searchLotes('')
    }
  }

  function validateForm () {
    clearErrors()
    let valid = true

    if (!form.cnsPaciente) {
      state.value.errors.cnsPaciente = 'Informe o CNS do paciente.'
      valid = false
    }
    if (!form.medicamentoId) {
      state.value.errors.medicamentoId = 'Selecione um medicamento.'
      valid = false
    }
    if (!form.loteId || !loteSelecionado.value) {
      state.value.errors.loteId = 'Lote inválido ou não selecionado.'
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
      const estoque = lote.quantidade_atual ?? (lote.quantidade_por_caixa * Number(lote.numero_caixa || 0))
      if (quantidadeTotal.value > estoque) {
        state.value.errors.numeroCaixas = `Estoque insuficiente. Disponível: ${estoque}, solicitado: ${quantidadeTotal.value}`
        valid = false
      }
    }

    return valid
  }

  function resetForm () {
    form.cnsPaciente = null
    form.nomePacienteSnapshot = null
    form.numeroReceita = null
    form.medicamentoId = null
    form.loteId = null
    form.nomeRemedioManual = null
    form.numeroCaixas = 1
    form.quantidadePorCaixa = 1
    form.motivo = 'Dispensa ao Paciente'
    form.dataSaida = new Date().toISOString().slice(0, 10)
    form.observacao = ''
    state.value.loteDetalhado = null
    state.value.lotesDisponiveisBusca = []
    state.value.lotesDisponiveisBusca = []
    clearErrors()
  }

  const idUsuarioResponsavel = 1

  function handleMasterPasswordCheck () {
    if (!validateForm()) return
    showConfirmPasswordDialog.value = true
    masterPassword.value = ''
    masterPasswordError.value = false
  }

  async function submitForm () {
    masterPasswordError.value = false

    const trimmedPassword = masterPassword.value.trim()

    if (trimmedPassword !== SYSTEM_SECRET_PASSWORD) {
      masterPasswordError.value = true
      snackbarColor.value = 'error'
      snackbarMessage.value = 'Senha-mestre incorreta. Tente novamente.'
      showSnackbar.value = true
      return
    }

    state.value.loading.submit = true
    showConfirmPasswordDialog.value = false

    try {
      const lote = loteSelecionado.value
      if (!lote) return

      const payload = {
        cns_paciente: form.cnsPaciente || '',
        nome_paciente: form.nomePacienteSnapshot || '',
        numero_receita: form.numeroReceita || '',
        tipo_saida: form.motivo,
        observacao: form.observacao?.trim() || '',
        quantidade: quantidadeTotal.value,
        numero_lote: lote.numero_lote || '',
        id_usuario_responsavel: Number(idUsuarioResponsavel),
      }

      const res = await fetch(`${API_BASE_URL}/saidas/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Pass': trimmedPassword,
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(API_TIMEOUT),
      })

      if (res.status === 401 || res.status === 403) {
        snackbarColor.value = 'error'
        snackbarMessage.value = 'Falha na autenticação (API). Senha incorreta.'
        showSnackbar.value = true
        showConfirmPasswordDialog.value = true
        return
      }

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}))
        console.error('Erro ao registrar saída', errBody)
        snackbarColor.value = 'error'
        snackbarMessage.value = `Erro no servidor: ${errBody.detail || res.statusText}`
        showSnackbar.value = true
        return
      }

      resetForm()
      snackbarColor.value = 'success'
      snackbarMessage.value = 'Saída registrada com sucesso!'
      showSnackbar.value = true
    } catch (error) {
      console.error(error)
      snackbarColor.value = 'error'
      snackbarMessage.value = 'Erro de rede ou timeout.'
      showSnackbar.value = true
    } finally {
      state.value.loading.submit = false
    }
  }

  watch(loteSelecionado, newVal => {
    if (newVal) {
      form.nomeRemedioManual = newVal.medicamento?.nome || 'Nome Indisponível'
      form.quantidadePorCaixa = newVal.quantidade_por_caixa || 1
      state.value.errors.loteId = null
    } else {
      form.nomeRemedioManual = null
      form.quantidadePorCaixa = 1
    }
    state.value.loteDetalhado = newVal
  })

  watch(() => form.medicamentoId, (newVal, oldVal) => {
    if (newVal !== oldVal) {
      form.loteId = null
      state.value.lotesDisponiveisBusca = []
      if (newVal) {
        searchLotes('')
      }
    }
  })

  watch(() => form.cnsPaciente, cns => {
    const cnsString = cns ? String(cns).trim() : ''
    form.nomePacienteSnapshot = cnsString.length >= 15 ? `Paciente - CNS ${cnsString.slice(0, 4)}...` : null
  })
</script>

<template>
  <v-container class="page-container pa-8 bg-gradient" fluid>

    <v-snackbar
      v-model="showSnackbar"
      :color="snackbarColor"
      location="top right"
      timeout="3000"
    >
      {{ snackbarMessage }}
      <template #actions>
        <v-btn
          color="white"
          variant="text"
          @click="showSnackbar = false"
        >
          Fechar
        </v-btn>
      </template>
    </v-snackbar>

    <v-dialog
      v-model="showConfirmPasswordDialog"
      max-width="400px"
      persistent
      transition="slide-y-transition"
    >
      <v-card class="modal-card pa-6" elevation="10" rounded="xl">
        <v-card-title class="text-h4 font-weight-bold text-center pa-0 mb-4">
          Confirmação
        </v-card-title>
        <p class="text-h6 text-slate-600 text-center mb-6">Confirme colocando a senha-mestre</p>

        <v-card-text>
          <v-text-field
            v-model="masterPassword"
            density="comfortable"
            :error="masterPasswordError"
            :error-messages="masterPasswordError ? 'Senha incorreta.' : ''"
            label="Senha-mestre"
            prepend-inner-icon="mdi-lock"
            rounded="lg"
            :type="'password'"
            variant="outlined"
            @keydown.enter="submitForm"
          />
        </v-card-text>

        <v-card-actions class="pa-0 d-flex justify-space-between">
          <v-btn
            class="modal-btn-cancel"
            color="#c25353"
            rounded="lg"
            size="large"
            variant="flat"
            @click="showConfirmPasswordDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            class="modal-btn-confirm"
            color="#3b5b76"
            :disabled="state.loading.submit"
            :loading="state.loading.submit"
            rounded="lg"
            size="large"
            variant="flat"
            @click="submitForm"
          >
            Concluir
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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

    <v-form @submit.prevent="handleMasterPasswordCheck">

      <v-card class="section-card mb-6" elevation="1" rounded="xl">
        <div class="section-body">
          <h2 class="section-title">Dados do Paciente:</h2>

          <v-row dense>
            <v-col cols="12">
              <label class="input-label">CNS:</label>
              <v-text-field
                v-model="form.cnsPaciente"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details="auto"
                placeholder="Digite o CNS do paciente"
                variant="solo"
              />
              <div v-if="state.errors.cnsPaciente" class="error-text">{{ state.errors.cnsPaciente }}</div>
            </v-col>

            <v-col cols="12">
              <label class="input-label">Nome do paciente:</label>
              <v-text-field
                bg-color="#f1f5f9"
                class="rounded-input"
                flat

                hide-details
                :model-value="form.nomePacienteSnapshot || ''"
                placeholder="Digite o nome completo do Paciente"
                variant="solo"
              />
            </v-col>

            <v-col cols="12">
              <label class="input-label">Número da receita (opcional):</label>
              <v-text-field
                v-model="form.numeroReceita"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details
                placeholder="Insira o número da receita"
                variant="solo"
              />
            </v-col>
          </v-row>
        </div>
      </v-card>
      <v-card class="section-card mb-6" elevation="1" rounded="xl">
        <div class="section-body">
          <h2 class="section-title">Informações do Remédio:</h2>

          <v-row dense>
            <v-col cols="12">
              <label class="input-label">Medicamento:</label>
              <v-autocomplete
                v-model="form.medicamentoId"
                bg-color="#f1f5f9"
                class="rounded-input"
                clearable
                flat
                hide-details="auto"
                item-title="nome"
                item-value="id_medicamento"
                :items="state.medicamentosItems"
                :loading="state.loading.medicamentos"
                placeholder="Digite o nome do medicamento para buscar e selecionar"
                variant="solo"
                @click:append-inner="handleOpenMedicamentoAutocomplete"
                @update:search="searchMedicamentos"
              />
              <div v-if="state.errors.medicamentoId" class="error-text">{{ state.errors.medicamentoId }}</div>
            </v-col>
          </v-row>

          <v-row dense>
            <v-col cols="12">
              <label class="input-label d-flex justify-space-between align-center">
                <span>Lote (ordenados por validade):</span>
                <span v-if="loteSelecionado" class="text-caption text-slate-500">
                  Val: {{ formatDate(loteSelecionado.data_validade) }}
                </span>
              </label>

              <v-autocomplete
                v-model="form.loteId"
                bg-color="#f1f5f9"
                class="rounded-input"
                clearable
                :disabled="!form.medicamentoId"
                flat
                hide-details="auto"
                item-title="title"
                item-value="value"
                :items="lotesFormatados"
                :loading="state.loading.lotes"
                :placeholder="form.medicamentoId ? 'Selecione o lote (os mais próximos do vencimento aparecem primeiro)' : 'Selecione um medicamento primeiro'"
                variant="solo"
                @click:append-inner="handleOpenLoteAutocomplete"
                @update:search="searchLotes"
              />

              <div v-if="state.errors.loteId" class="error-text">{{ state.errors.loteId }}</div>
            </v-col>
          </v-row>

          <v-row dense>
            <v-col cols="12">
              <div class="d-flex justify-space-between align-center">
                <label class="input-label mb-0">Caixas:</label>
                <div class="stepper-wrapper">
                  <div class="custom-stepper" :class="{ 'stepper-disabled': !loteSelecionado }">
                    <v-btn
                      :disabled="!loteSelecionado || form.numeroCaixas <= 1"
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
                      :disabled="!loteSelecionado"
                      min="1"
                      type="number"
                    >

                    <v-btn
                      :disabled="!loteSelecionado"
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

          <v-row dense>
            <v-col cols="12" md="6">
              <label class="input-label">Quantidade por caixa:</label>
              <v-text-field
                v-model.number="form.quantidadePorCaixa"
                bg-color="#f1f5f9"
                class="rounded-input"
                :disabled="!loteSelecionado"
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
                    {{
                      loteSelecionado.quantidade_atual ?? (loteSelecionado.quantidade_por_caixa * Number(loteSelecionado.numero_caixa || 0))
                    }} unidades
                  </span>
                </div>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-card>
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
