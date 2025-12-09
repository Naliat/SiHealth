<script lang="ts" setup>
  import { computed, reactive } from 'vue'
  import { registrarEntrada } from '@/services/movimentacaoService'

  const form = reactive({
    // Use loteId (numeric) to match backend expectation for id_lote
    loteId: '' as string | number,
    codigo: '',
    nome: '',
    principioAtivo: '',
    tarja: null as string | null,
    caixas: 1,
    qtdPorCaixa: 1,
    dosagem: '',
    dosagemUnidade: 'mg',
    lote: '',
    validade: '',
    fabricante: '',
    registroMs: '',
  })

  const tarjaOptions = ['Sem Tarja', 'Tarja Amarela', 'Tarja Vermelha', 'Tarja Preta']
  const unidadeOptions = ['mg', 'g', 'ml', 'mcg']

  const state = reactive({
    loading: false,
    errors: {
      loteId: null as string | null,
      quantidade: null as string | null,
    },
    message: null as string | null,
  })

  const idUsuarioResponsavel = 1 // temporário, conforme frontend existente

  const quantidadeTotal = computed(() => {
    const caixas = Number(form.caixas) || 0
    const qtd = Number(form.qtdPorCaixa) || 0
    return caixas * qtd
  })

  function updateNumber (field: 'caixas' | 'qtdPorCaixa', delta: number) {
    const current = Number(form[field]) || 0
    const newValue = current + delta
    form[field] = Math.max(newValue, 1)
  }

  function onNumberInput (field: 'caixas' | 'qtdPorCaixa', value: any) {
    const n = Number(value)
    form[field] = isNaN(n) || n < 1 ? 1 : Math.floor(n)
  }

  function clearErrors () {
    state.errors.loteId = null
    state.errors.quantidade = null
    state.message = null
  }

  function validateForm () {
    clearErrors()
    let valid = true

    if (!form.loteId && form.loteId !== 0) {
      state.errors.loteId = 'Informe o ID do lote'
      valid = false
    } else if (Number.isNaN(Number(form.loteId))) {
      state.errors.loteId = 'ID do lote inválido'
      valid = false
    }

    if (quantidadeTotal.value < 1) {
      state.errors.quantidade = 'Quantidade deve ser >= 1'
      valid = false
    }

    return valid
  }

  function clearForm () {
    form.loteId = ''
    form.codigo = ''
    form.nome = ''
    form.principioAtivo = ''
    form.tarja = null
    form.caixas = 1
    form.qtdPorCaixa = 1
    form.dosagem = ''
    form.dosagemUnidade = 'mg'
    form.lote = ''
    form.validade = ''
    form.fabricante = ''
    form.registroMs = ''
    clearErrors()
  }

  async function submitForm () {
    if (!validateForm()) return

    state.loading = true
    state.message = null

    try {
      const payload = {
        id_lote: Number(form.loteId),
        quantidade: Number(quantidadeTotal.value),
        id_usuario: Number(idUsuarioResponsavel),
        fornecedor: form.fabricante?.trim() || undefined,
      } as any

      const data = await registrarEntrada(payload)
      console.log('Entrada registrada com sucesso', data)
      state.message = 'Entrada registrada com sucesso'
      clearForm()
    } catch (error: any) {
      console.error('Erro ao registrar entrada', error)
      state.message = error?.message || 'Erro ao registrar entrada'
    } finally {
      state.loading = false
    }
  }
</script>

<template>
  <v-container class="page-container pa-8 bg-gradient" fluid>
    <div class="d-flex justify-space-between align-start mb-8">
      <div>
        <h1 class="text-h3 font-weight-bold text-slate-900 mb-2">Registrar Entrada</h1>
        <p class="text-h6 text-slate-600">Registro de entrada no estoque</p>
      </div>

      <v-btn class="user-btn" variant="text">
        <v-icon start>mdi-account-circle</v-icon>
        Usuário
        <v-icon end size="small">mdi-chevron-down</v-icon>
      </v-btn>
    </div>

    <v-form @submit.prevent="submitForm">

      <!-- 1) Informações do Lote (top card in image) -->
      <v-card class="mb-6 pa-6 inner-card" elevation="2" rounded="xl">
        <h2 class="section-title mb-6">Informações do Lote:</h2>

        <v-row dense>
          <v-col cols="12" md="7">
            <div class="mb-4">
              <label class="input-label"># Lote (ID):</label>
              <v-text-field
                v-model="form.loteId"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details
                placeholder="ID numérico do lote"
                type="number"
                variant="solo"
              />
              <div v-if="state.errors.loteId" class="error-text">{{ state.errors.loteId }}</div>
            </div>

            <div class="mb-4">
              <label class="input-label"><v-icon class="mr-1" icon="mdi-domain" size="small" /> Fabricante:</label>
              <v-text-field
                v-model="form.fabricante"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details
                variant="solo"
              />
            </div>

            <div>
              <label class="input-label"><v-icon class="mr-1" icon="mdi-file-document-outline" size="small" /> Registro MS:</label>
              <v-text-field
                v-model="form.registroMs"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details
                variant="solo"
              />
            </div>
          </v-col>

          <v-col class="pl-md-8" cols="12" md="5">
            <div class="mb-4">
              <label class="input-label"><v-icon class="mr-1" icon="mdi-calendar" size="small" /> Validade:</label>
              <v-text-field
                v-model="form.validade"
                bg-color="#f1f5f9"
                class="rounded-input"
                flat
                hide-details
                type="date"
                variant="solo"
              />
            </div>

            <div class="mb-4">
              <label class="input-label"><v-icon class="mr-1" icon="mdi-package-variant" size="small" /> Caixas:</label>
              <div class="custom-stepper">
                <v-btn icon size="x-small" variant="text" @click="updateNumber('caixas', -1)">
                  <v-icon>mdi-chevron-left</v-icon>
                </v-btn>
                <input
                  v-model="form.caixas"
                  class="stepper-input"
                  min="1"
                  type="number"
                  @input="(e) => onNumberInput('caixas', (e.target as HTMLInputElement).value)"
                >
                <v-btn icon size="x-small" variant="text" @click="updateNumber('caixas', 1)">
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </div>
            </div>

            <div class="mb-2">
              <label class="input-label"><v-icon class="mr-1" icon="mdi-grid" size="small" /> Quantidade:</label>
              <div class="d-flex align-center">
                <div class="custom-stepper mr-2">
                  <v-btn icon size="x-small" variant="text" @click="updateNumber('qtdPorCaixa', -1)">
                    <v-icon>mdi-chevron-left</v-icon>
                  </v-btn>
                  <input
                    v-model="form.qtdPorCaixa"
                    class="stepper-input"
                    min="1"
                    type="number"
                    @input="(e) => onNumberInput('qtdPorCaixa', (e.target as HTMLInputElement).value)"
                  >
                  <v-btn icon size="x-small" variant="text" @click="updateNumber('qtdPorCaixa', 1)">
                    <v-icon>mdi-chevron-right</v-icon>
                  </v-btn>
                </div>
                <span class="text-caption text-slate-600">Unidades por Caixa</span>
              </div>
              <div v-if="state.errors.quantidade" class="error-text">{{ state.errors.quantidade }}</div>
            </div>

            <div class="mt-4">
              <div class="text-caption">Quantidade total: <strong>{{ quantidadeTotal }}</strong></div>
            </div>
          </v-col>
        </v-row>
      </v-card>

      <v-card class="mb-6 pa-6 inner-card" elevation="2" rounded="xl">
        <h2 class="section-title mb-6">Dados do Remédio:</h2>

        <v-row dense>
          <v-col cols="12" md="8">
            <div class="mb-4">
              <label class="input-label"><v-icon class="mr-1" icon="mdi-pill" size="small" /> Nome do remédio:</label>
              <v-text-field
                v-model="form.nome"
                bg-color="#f1f5f9"
                flat
                class="rounded-input"
                hide-details
                placeholder="Digite o nome"
                variant="solo"
              />
            </div>

            <div class="mb-4">
              <label class="input-label"><v-icon class="mr-1" icon="mdi-flask" size="small" /> Princípio Ativo:</label>
              <v-text-field
                v-model="form.principioAtivo"
                bg-color="#f1f5f9"
                flat
                class="rounded-input"
                hide-details
                placeholder="Digite o princípio ativo"
                variant="solo"
              />
            </div>

            <div>
              <label class="input-label"><v-icon class="mr-1" icon="mdi-lock" size="small" /> Tarja:</label>
              <v-select
                v-model="form.tarja"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
                :items="tarjaOptions"
                menu-icon="mdi-chevron-down"
                placeholder="Selecione"
variant="solo"
              />
            </div>
          </v-col>

          <v-col class="pl-md-8" cols="12" md="4">
            <div>
              <label class="input-label"><v-icon class="mr-1" icon="mdi-eyedropper" size="small" /> Dosagem:</label>
              <div class="d-flex ga-2">
                <v-text-field
                  v-model="form.dosagem"
                  bg-color="#f1f5f9"
                  flat
                  class="rounded-input flex-grow-1"
                  hide-details
                  placeholder="00"
                  variant="solo"
                />
                <v-select
                  v-model="form.dosagemUnidade"
                  bg-color="#f1f5f9"
                  flat
                  class="rounded-input"
                  hide-details
                  :items="unidadeOptions"
                  menu-icon="mdi-chevron-down"
                  style="max-width: 100px;"
variant="solo"
                />
              </div>
            </div>
          </v-col>
        </v-row>
      </v-card>

      <div class="d-flex justify-end gap-4">
        <v-btn
          class="cancel-btn"
          color="red"
          :disabled="state.loading"
          rounded="lg"
          size="large"
          variant="tonal"
          @click="clearForm"
        >Cancelar</v-btn>

        <v-btn
          class="concluir-btn px-10"
          color="slate600"
          :loading="state.loading"
          rounded="lg"
          size="large"
          type="submit"
        >Concluir</v-btn>
      </div>

      <div v-if="state.message" class="mt-4">
        <v-alert dense text="true" type="info">{{ state.message }}</v-alert>
      </div>

    </v-form>
  </v-container>
</template>

<style scoped>

.bg-gradient {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
}

.breadcrumb {
  color: #94a3b8; /* slate-400 */
}

.error-text {
  color: #b91c1c;
  font-size: 0.85rem;
  margin-top: 6px;
}

.text-slate-900 { color: #0f172a; }
.text-slate-600 { color: #475569; }

.subtitle-underline {
  display: inline-block;
  position: relative;
  padding-bottom: 6px;
}
.subtitle-underline::after {
  content: '';
  position: absolute;
  left: 0;
  right: 50%;
  bottom: 0;
  height: 3px;
  background-color: #2563eb;
  border-radius: 2px;
  opacity: 0.9;
}

.section-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
}

.user-btn {
  color: #475569 !important;
  text-transform: none;
  letter-spacing: normal;
}

.inner-card {
  background: #f8fbfd;
  border: 1px solid #e6f0f7;
  padding: 18px;
  border-radius: 12px;
}

.input-label {
  display: block;
  font-weight: 700;
  font-size: 0.9rem;
  color: #0f172a;
  margin-bottom: 8px;
}

.rounded-input :deep(.v-field) {
  border-radius: 8px !important;
}

.custom-stepper {
  display: inline-flex;
  align-items: center;
  background-color: #f1f5f9;
  border-radius: 8px;
  padding: 4px;
  height: 44px;
}

.stepper-input {
  width: 56px;
  text-align: center;
  font-weight: 600;
  color: #475569;
  border: none;
  outline: none;
  background: transparent;
  appearance: textfield;
}

.stepper-input::-webkit-outer-spin-button,
.stepper-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Botões */
.concluir-btn {
  background-color: #1f5a8a !important;
  color: white !important;
  font-weight: 600;
  text-transform: none;
}
.cancel-btn {
  background-color: #b91c1c !important; /* red-700 */
  color: white !important;
  font-weight: 600;
  text-transform: none;
}

</style>
