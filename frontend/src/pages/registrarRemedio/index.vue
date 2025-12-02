<script lang="ts" setup>
import { ref, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const API_MEDICAMENTOS = "http://localhost:8000/api/v1/medicamentos/";
const router = useRouter();
const form = ref({
  nomeRemedio: "",
  principioAtivo: "",
  tarja: "",
  dosagem: "",
  fabricante: "",
  lote: "", 
  
  registroMS: "", 
  codigoProduto: "" as string | number, 
  caixas: 1, 
  unidadesPorCaixa: 1, 
  dataFabricacao: "" as string | null,
  validade: "" as string | null, 
});

const isLoading = ref(false);
const error = ref("");

const tarjaOptions = [
  "Preta",
  "Vermelha (Com Retenção)",
  "Amarela",
  "Isenta",
];

const validarFormulario = () => {
  if (!String(form.value.nomeRemedio ?? "").trim()) {
    error.value = "Nome do remédio é obrigatório";
    return false;
  }
  if (!String(form.value.principioAtivo ?? "").trim()) {
    error.value = "Princípio ativo é obrigatório";
    return false;
  }
  if (!form.value.tarja) {
    error.value = "Tarja é obrigatória";
    return false;
  }
  if (!String(form.value.dosagem ?? "").trim()) {
    error.value = "Dosagem é obrigatória";
    return false;
  }
  if (!String(form.value.fabricante ?? "").trim()) {
    error.value = "Fabricante é obrigatório";
    return false;
  }
  if (!String(form.value.lote ?? "").trim()) {
    error.value = "Número do lote é obrigatório";
    return false;
  }
  
  return true;
};

const concluir = async () => {
  error.value = "";

  if (!validarFormulario()) return;
  isLoading.value = true;
  const payload = {
    nome: String(form.value.nomeRemedio ?? "").trim(),
    principio_ativo: String(form.value.principioAtivo ?? "").trim(),
    tarja: form.value.tarja,
    dosagem: String(form.value.dosagem ?? "").trim(),
    fabricante: String(form.value.fabricante ?? "").trim(),

  };

  try {
    const response = await axios.post(API_MEDICAMENTOS, payload);
    
    alert(`Medicamento '${response.data.nomeRemedio || response.data.nome}' cadastrado com sucesso!`);
    router.push("/medicamentos");
  } catch (err: any) {
    console.error("Erro no cadastro:", err);
    const apiErrorDetail = err.response?.data?.detail;
    if (Array.isArray(apiErrorDetail) && apiErrorDetail.length > 0) {
        error.value = `Erro de validação da API: ${apiErrorDetail.map((e: any) => `${e.loc.join('.')}: ${e.msg}`).join(' | ')}`;
    } else {
        error.value = apiErrorDetail ?? "Falha na comunicação com o servidor ou dados inválidos.";
    }
  } finally {
    isLoading.value = false;
  }
};

const cancelar = () => {
  if (confirm("Tem certeza que deseja cancelar o registro?")) {
    router.push("/");
  }
};
</script>

<template>
  <v-container fluid class="pa-6" style="background-color: #f0f4f7; min-height: 100vh;">
    <h1 class="text-h4 mb-2 text-black font-weight-bold">Registrar Remédio</h1>
    <p class="text-subtitle-1 mb-6 text-medium-emphasis">Registro de novo medicamento no sistema</p>

    <v-card class="pa-6" rounded="lg">
      <v-form @submit.prevent="concluir">
        <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

        <v-card-title class="text-h6 font-weight-bold pa-0 mb-4" style="color: #3b5b76;">
          Dados do Remédio:
        </v-card-title>

        <v-row>
          <v-col cols="12" md="6">
            
            <v-text-field
              v-model="form.nomeRemedio"
              label="Nome do Remédio:"
              prepend-icon="mdi-pill"
              variant="outlined"
              density="compact"
              required
              :disabled="isLoading"
            />

           
            <v-text-field
              v-model="form.principioAtivo"
              label="Princípio Ativo:"
              prepend-icon="mdi-flask-outline"
              variant="outlined"
              density="compact"
              required
              :disabled="isLoading"
            />

           
            <v-select
              v-model="form.tarja"
              :items="tarjaOptions"
              label="Tarja:"
              prepend-icon="mdi-lock"
              variant="outlined"
              density="compact"
              required
              :disabled="isLoading"
            />
          </v-col>

          <v-col cols="12" md="6">
  
            <v-text-field
              v-model="form.dosagem"
              label="Dosagem:"
              prepend-icon="mdi-weight-kilogram"
              suffix="mg"
              variant="outlined"
              density="compact"
              required
              :disabled="isLoading"
            />
            
          
            <v-text-field
              v-model="form.fabricante"
              label="Fabricante:"
              prepend-icon="mdi-factory"
              variant="outlined"
              density="compact"
              required
              :disabled="isLoading"
            />
            <v-text-field
                v-model="form.lote"
                label="# Lote:"
                prepend-icon="mdi-barcode"
                variant="outlined"
                density="compact"
                required
                :disabled="isLoading"
                class="mt-4"
            />
          </v-col>
        </v-row>

        <v-divider class="my-6" />

        <div class="d-flex justify-end">
          <v-btn color="#a04442" variant="flat" @click="cancelar" class="mr-4 text-white" :disabled="isLoading" style="text-transform: none;">Cancelar</v-btn>
          <v-btn type="submit" color="#3b5b76" :loading="isLoading" :disabled="isLoading" class="text-white" style="text-transform: none;">
            <span v-if="!isLoading">Registrar Medicamento</span>
            <span v-else>Cadastrando...</span>
          </v-btn>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>