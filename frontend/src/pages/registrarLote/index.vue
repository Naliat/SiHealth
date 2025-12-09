<script lang="ts" setup>
  import axios from 'axios'
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router'

  const API_URL = 'http://localhost:8000/api/v1/lotes/'
  const API_MEDICAMENTOS = 'http://localhost:8000/api/v1/medicamentos/'

  // FORM
  const form = ref({
    codigoProduto: '',
    nomeRemedio: '',
    principioAtivo: '',
    tarja: '',
    caixas: 1,
    unidadesPorCaixa: 1,
    dosagem: '',
    lote: '',
    fabricante: '',
    registroMS: '',
    validade: null as string | null,
  })

  const isLoading = ref(false)
  const error = ref('')
  const isSearching = ref(false)

  const autocompleteOptions = ref<string[]>([])
  const medicamentosCache = ref<any[]>([])
  const cacheLoaded = ref(false)

  const tarjaOptions = ['Preta', 'Vermelha', 'Vermelha (Com Retenção)', 'Amarela', 'Sem Tarja', 'Isenta']

  const router = useRouter()

  const quantidadeTotal = computed(() => {
    return (form.value.caixas || 0) * (form.value.unidadesPorCaixa || 0)
  })

  async function loadMedicamentos () {
    if (cacheLoaded.value) return

    isSearching.value = true

    try {
      const response = await axios.get(API_MEDICAMENTOS)
      medicamentosCache.value = response.data

      autocompleteOptions.value = medicamentosCache.value.map(
        (item: any) => item.nome,
      )

      cacheLoaded.value = true
    } catch (error_) {
      console.error('Erro ao carregar medicamentos:', error_)
    } finally {
      isSearching.value = false
    }
  }

  async function searchRemedio (query: string) {
    if (!cacheLoaded.value) {
      await loadMedicamentos()
    }

    autocompleteOptions.value = medicamentosCache.value
      .filter((m: any) =>
        m.nome.toLowerCase().includes(query.toLowerCase()),
      )
      .map((m: any) => m.nome)
  }

  function onSelectAutocomplete (selected: string) {
    const med = medicamentosCache.value.find(item => item.nome === selected)
    if (!med) return

    form.value.nomeRemedio = med.nome
    form.value.principioAtivo = med.principio_ativo
    form.value.tarja = med.tarja
    form.value.dosagem = med.dosagem
    form.value.fabricante = med.fabricante
    form.value.codigoProduto = med.id_medicamento
  }

  async function concluir () {
    isLoading.value = true
    error.value = ''

    const payload = {
      numero_lote: form.value.lote || null,
      numero_caixa: String(form.value.caixas || 1),
      quantidade_por_caixa: form.value.unidadesPorCaixa || 1,
      quantidade_inicial: quantidadeTotal.value || 0,
      data_fabricacao: null,
      data_validade: form.value.validade || null,
      id_medicamento: form.value.codigoProduto || null,
    }

    try {
      const response = await axios.post(API_URL, payload)
      alert('Lote registrado com sucesso!')
      router.push('/medicamentos')
    } catch (error_: any) {
      console.error('Erro no cadastro:', error_)
      error.value = error_.response?.data?.detail || 'Erro ao enviar dados.'
    } finally {
      isLoading.value = false
    }
  }

  function cancelar () {
    if (confirm('Tem certeza que deseja cancelar o registro?')) {
      router.push('/')
    }
  }
</script>

<template>
  <v-container class="pa-6" fluid style="background-color: #f0f4f7; min-height: 100vh;">

    <h1 class="text-h4 mb-2 text-black font-weight-bold">Registrar Entrada</h1>
    <p class="text-subtitle-1 mb-6 text-medium-emphasis">Registro de entrada no estoque</p>

    <v-card class="pa-6" rounded="lg">
      <v-form @submit.prevent="concluir">

        <v-alert v-if="error" class="mb-4" type="error">{{ error }}</v-alert>

        <v-card-title class="text-h6 font-weight-bold pa-0 mb-4" style="color: #3b5b76;">
          Medicamento:
        </v-card-title>

        <v-autocomplete
          v-model="form.nomeRemedio"
          density="compact"
          :items="autocompleteOptions"
          label="Nome do Remédio"
          :loading="isSearching"
          prepend-icon="mdi-pill"
          variant="outlined"
          @focus="loadMedicamentos"
          @update:model-value="onSelectAutocomplete"
          @update:search="searchRemedio"
        />
        <v-row class="mt-4">
          <v-col cols="12" md="6">
            <v-text-field v-model="form.principioAtivo" label="Princípio Ativo" prepend-icon="mdi-flask-outline" variant="outlined" />
            <v-select
              v-model="form.tarja"
              :items="tarjaOptions"
              label="Tarja"
              prepend-icon="mdi-lock"
              variant="outlined"
            />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="form.dosagem"
              label="Dosagem"
              prepend-icon="mdi-weight-kilogram"
              suffix="mg"
              variant="outlined"
            />
            <input v-model="form.codigoProduto" type="hidden">
          </v-col>
        </v-row>

        <v-divider class="my-6" />

        <v-card-title class="text-h6 font-weight-bold pa-0 mb-4" style="color: #3b5b76;">
          Informações do Lote:
        </v-card-title>

        <v-row>
          <v-col cols="12" md="6">
            <v-text-field v-model="form.lote" label="# Lote" prepend-icon="mdi-barcode" variant="outlined" />
            <v-text-field v-model="form.fabricante" label="Fabricante" prepend-icon="mdi-factory" variant="outlined" />
            <v-text-field v-model="form.registroMS" label="Registro MS" prepend-icon="mdi-file-certificate-outline" variant="outlined" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="form.validade"
              label="Validade"
              prepend-icon="mdi-calendar"
              type="date"
              variant="outlined"
            />
            <v-text-field
              v-model.number="form.caixas"
              label="Caixas"
              min="1"
              prepend-icon="mdi-inbox-multiple"
              type="number"
              variant="outlined"
            />

            <v-row dense>
              <v-col cols="6">
                <v-text-field
                  disabled
                  label="Quantidade Total"
                  :model-value="quantidadeTotal"
                  prepend-icon="mdi-counter"
                  variant="outlined"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="form.unidadesPorCaixa"
                  label="Unidades por Caixa"
                  min="1"
                  type="number"
                  variant="outlined"
                />
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <v-divider class="my-6" />

        <div class="d-flex justify-end">
          <v-btn class="mr-4 text-white" color="#a04442" @click="cancelar">Cancelar</v-btn>
          <v-btn class="text-white" color="#3b5b76" :loading="isLoading" type="submit">Concluir</v-btn>
        </div>

      </v-form>
    </v-card>
  </v-container>
</template>
