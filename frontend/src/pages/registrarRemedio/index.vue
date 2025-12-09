<script lang="ts" setup>
  import axios from 'axios'
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router'

  const API_MEDICAMENTOS = 'http://localhost:8000/api/v1/medicamentos/'
  const router = useRouter()
  const form = ref({
    nomeRemedio: '',
    principioAtivo: '',
    tarja: '',
    dosagem: '',
    fabricante: '',
    lote: '',

    registroMS: '',
    codigoProduto: '' as string | number,
    caixas: 1,
    unidadesPorCaixa: 1,
    dataFabricacao: '' as string | null,
    validade: '' as string | null,
  })

  const isLoading = ref(false)
  const error = ref('')

  const tarjaOptions = [
    'Preta',
    'Vermelha (Com Retenção)',
    'Amarela',
    'Isenta',
  ]

  function validarFormulario () {
    if (!String(form.value.nomeRemedio ?? '').trim()) {
      error.value = 'Nome do remédio é obrigatório'
      return false
    }
    if (!String(form.value.principioAtivo ?? '').trim()) {
      error.value = 'Princípio ativo é obrigatório'
      return false
    }
    if (!form.value.tarja) {
      error.value = 'Tarja é obrigatória'
      return false
    }
    if (!String(form.value.dosagem ?? '').trim()) {
      error.value = 'Dosagem é obrigatória'
      return false
    }
    if (!String(form.value.fabricante ?? '').trim()) {
      error.value = 'Fabricante é obrigatório'
      return false
    }
    if (!String(form.value.lote ?? '').trim()) {
      error.value = 'Número do lote é obrigatório'
      return false
    }

    return true
  }

  async function concluir () {
    error.value = ''

    if (!validarFormulario()) return
    isLoading.value = true
    const payload = {
      nome: String(form.value.nomeRemedio ?? '').trim(),
      principio_ativo: String(form.value.principioAtivo ?? '').trim(),
      tarja: form.value.tarja,
      dosagem: String(form.value.dosagem ?? '').trim(),
      fabricante: String(form.value.fabricante ?? '').trim(),

    }

    try {
      const response = await axios.post(API_MEDICAMENTOS, payload)

      alert(`Medicamento '${response.data.nomeRemedio || response.data.nome}' cadastrado com sucesso!`)
      router.push('/medicamentos')
    } catch (error_: any) {
      console.error('Erro no cadastro:', error_)
      const apiErrorDetail = error_.response?.data?.detail
      error.value = Array.isArray(apiErrorDetail) && apiErrorDetail.length > 0 ? `Erro de validação da API: ${apiErrorDetail.map((e: any) => `${e.loc.join('.')}: ${e.msg}`).join(' | ')}` : apiErrorDetail ?? 'Falha na comunicação com o servidor ou dados inválidos.'
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
    <h1 class="text-h4 mb-2 text-black font-weight-bold">Registrar Remédio</h1>
    <p class="text-subtitle-1 mb-6 text-medium-emphasis">Registro de novo medicamento no sistema</p>

    <v-card class="pa-6" rounded="lg">
      <v-form @submit.prevent="concluir">
        <v-alert v-if="error" class="mb-4" type="error">{{ error }}</v-alert>

        <v-card-title class="text-h6 font-weight-bold pa-0 mb-4" style="color: #3b5b76;">
          Dados do Remédio:
        </v-card-title>

        <v-row>
          <v-col cols="12" md="6">

            <v-text-field
              v-model="form.nomeRemedio"
              density="compact"
              :disabled="isLoading"
              label="Nome do Remédio:"
              prepend-icon="mdi-pill"
              required
              variant="outlined"
            />

            <v-text-field
              v-model="form.principioAtivo"
              density="compact"
              :disabled="isLoading"
              label="Princípio Ativo:"
              prepend-icon="mdi-flask-outline"
              required
              variant="outlined"
            />

            <v-select
              v-model="form.tarja"
              density="compact"
              :disabled="isLoading"
              :items="tarjaOptions"
              label="Tarja:"
              prepend-icon="mdi-lock"
              required
              variant="outlined"
            />
          </v-col>

          <v-col cols="12" md="6">

            <v-text-field
              v-model="form.dosagem"
              density="compact"
              :disabled="isLoading"
              label="Dosagem:"
              prepend-icon="mdi-weight-kilogram"
              required
              suffix="mg"
              variant="outlined"
            />

            <v-text-field
              v-model="form.fabricante"
              density="compact"
              :disabled="isLoading"
              label="Fabricante:"
              prepend-icon="mdi-factory"
              required
              variant="outlined"
            />
            <v-text-field
              v-model="form.lote"
              class="mt-4"
              density="compact"
              :disabled="isLoading"
              label="# Lote:"
              prepend-icon="mdi-barcode"
              required
              variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-6" />

        <div class="d-flex justify-end">
          <v-btn
            class="mr-4 text-white"
            color="#a04442"
            :disabled="isLoading"
            style="text-transform: none;"
            variant="flat"
            @click="cancelar"
          >Cancelar</v-btn>
          <v-btn
            color="#3b5b76"
            class="text-white"
            :disabled="isLoading"
            :loading="isLoading"
            style="text-transform: none;"
            type="submit"
          >
            <span v-if="!isLoading">Registrar Medicamento</span>
            <span v-else>Cadastrando...</span>
          </v-btn>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>
