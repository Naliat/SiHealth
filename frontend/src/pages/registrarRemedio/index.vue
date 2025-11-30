<script lang="ts" setup>
import { ref, computed } from 'vue'; 
import axios from 'axios'; 
import { useRouter } from 'vue-router'; 

// URL da API (mantida do código original)
const API_URL = "http://localhost:8000/remedios"; 

const router = useRouter();
const form = ref({
    // Campos visíveis na interface
    nomeRemedio: '',
    principioAtivo: '',
    tarja: '',
    dosagem: '',
    lote: '',
    fabricante: '',

    // Campos mantidos no script e payload da API, mas ocultos na interface para o layout atual
    codigoProduto: '', 
    caixas: 1, 
    unidadesPorCaixa: 1, 
    registroMS: '',
    validade: null as string | null, 
});

const isLoading = ref(false);
const error = ref('');

const tarjaOptions = ['Preta', 'Vermelha (Com Retenção)', 'Amarela', 'Isenta'];

// `quantidadeTotal` mantido para lógica de API, embora não exibido
const quantidadeTotal = computed(() => {
     return (form.value.caixas || 0) * (form.value.unidadesPorCaixa || 0);
});

const concluir = async () => {
    isLoading.value = true;
    error.value = '';

    const payload = {
        // Todos os campos são enviados, incluindo os ocultos
        codigoProduto: form.value.codigoProduto,
        nomeRemedio: form.value.nomeRemedio,
        principioAtivo: form.value.principioAtivo,
        tarja: form.value.tarja,
        caixas: form.value.caixas,
        unidadesPorCaixa: form.value.unidadesPorCaixa,
        dosagem: form.value.dosagem,
        lote: form.value.lote,
        fabricante: form.value.fabricante,
        registroMS: form.value.registroMS,
        validade: form.value.validade || null, 
    };

    try {
        const response = await axios.post(API_URL, payload);
        
        if (response.status === 201) {
            // Usando alert() conforme a lógica original
            alert(`Medicamento '${response.data.nomeRemedio}' cadastrado com sucesso!`);
            router.push('/medicamentos'); 
        }

    } catch (err: any) {
        console.error("Erro no cadastro:", err);
        
        if (err.response && err.response.data && err.response.data.detail) {
            error.value = `Erro: ${err.response.data.detail}`;
        } else {
            error.value = 'Falha na comunicação com o servidor ou dados inválidos.';
        }
    } finally {
        isLoading.value = false;
    }
};

const cancelar = () => {
    // Usando confirm() conforme a lógica original
    if (confirm('Tem certeza que deseja cancelar o registro?')) { 
        router.push('/'); 
    }
};
</script>

<template>
    <!-- Fundo cinza claro para o container principal -->
    <v-container fluid class="pa-6" style="background-color: #f0f4f7; min-height: 100vh;">
        <!-- Título principal -->
        <h1 class="text-h4 mb-2 text-black font-weight-bold">Registrar Remédio</h1>
        <p class="text-subtitle-1 mb-6 text-medium-emphasis">Registro de novo remédio</p>

        <!-- Card principal com fundo branco e bordas arredondadas -->
        <v-card class="pa-6" rounded="lg">
            
            <v-form @submit.prevent="concluir">
            
                <!-- Mensagem de Erro -->
                <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

                <!-- Seção Única: DADOS DO REMÉDIO -->
                <v-card-title class="text-h6 font-weight-bold pa-0 mb-4" style="color: #3b5b76;">Dados do Remédio:</v-card-title>
                
                <v-row>
                    <!-- Coluna Esquerda: Nome, Princípio Ativo, Tarja -->
                    <v-col cols="12" md="6">
                        <v-text-field
                            v-model="form.nomeRemedio"
                            label="Nome do remédio:"
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

                    <!-- Coluna Direita: Dosagem, Lote, Fabricante -->
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
                            v-model="form.lote"
                            label="# Lote:"
                            prepend-icon="mdi-barcode"
                            variant="outlined"
                            density="compact"
                            required
                            :disabled="isLoading"
                            class="mt-4"
                        />
                        <v-text-field
                            v-model="form.fabricante"
                            label="Fabricante:"
                            prepend-icon="mdi-factory"
                            variant="outlined"
                            density="compact"
                            required
                            :disabled="isLoading"
                            class="mt-4"
                        />
                        
                        <!-- Campos Ocultos (necessários para o payload da API, mas invisíveis no layout) -->
                        <input type="hidden" v-model="form.codigoProduto">
                        <input type="hidden" v-model="form.caixas">
                        <input type="hidden" v-model="form.unidadesPorCaixa">
                        <input type="hidden" v-model="form.registroMS">
                        <input type="hidden" v-model="form.validade">
                    </v-col>
                </v-row>
                
                <v-divider class="my-6"/>

                <!-- Botões de Ação -->
                <div class="d-flex justify-end">
                    <v-btn 
                        color="#a04442" 
                        variant="flat" 
                        @click="cancelar" 
                        class="mr-4 text-white" 
                        :disabled="isLoading"
                        style="text-transform: none;"
                    >
                        Cancelar
                    </v-btn>
                    <v-btn 
                        type="submit" 
                        color="#3b5b76" 
                        :loading="isLoading" 
                        :disabled="isLoading"
                        class="text-white"
                        style="text-transform: none;"
                    >
                        Concluir
                    </v-btn>
                </div>
            </v-form>
        </v-card>
    </v-container>
</template>

<style scoped>
/* Estilos mantidos, caso haja necessidade futura de customização */
</style>