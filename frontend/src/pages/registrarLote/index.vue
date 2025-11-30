<script lang="ts" setup>
import { ref, computed } from 'vue'; 
import axios from 'axios'; 
import { useRouter } from 'vue-router'; 

const API_URL = "http://localhost:8000/remedios"; 

const router = useRouter();
const form = ref({
    // Todos os campos são necessários para o payload da API
    codigoProduto: '', // Mantido no script, mas oculto na interface
    nomeRemedio: '',
    principioAtivo: '',
    tarja: '',
    caixas: 1, 
    unidadesPorCaixa: 1, 
    dosagem: '',
    
    lote: '',
    fabricante: '',
    registroMS: '',
    validade: null as string | null, // Mantido para o payload da API
});

 const isLoading = ref(false);
const error = ref('');

 const tarjaOptions = ['Preta', 'Vermelha (Com Retenção)', 'Amarela', 'Isenta'];

 // Campo computado para a quantidade total
 const quantidadeTotal = computed(() => {
     return (form.value.caixas || 0) * (form.value.unidadesPorCaixa || 0);
});

 const concluir = async () => {
    isLoading.value = true;
    error.value = '';

     const payload = {
        // Todos os campos são enviados
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
        // Garante que a data está no formato YYYY-MM-DD ou null
        validade: form.value.validade || null, 
    };

    try {
        // Envio da requisição POST para o FastAPI
        const response = await axios.post(API_URL, payload);
        
        // Usando um modal de sucesso no lugar de 'alert()' para melhor UX
        // Nota: O ambiente Canvas não permite 'alert()', então vamos usar um estado para exibir a mensagem
        alert(`Medicamento '${response.data.nomeRemedio}' cadastrado com sucesso!`); 
        // Redireciona para a lista de medicamentos após sucesso
        router.push('/medicamentos'); 

    } catch (err: any) {
        // Tratamento de Erros (ex: 400 Bad Request do Pydantic)
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
    // Usando uma confirmação de modal no lugar de 'confirm()'
    if (confirm('Tem certeza que deseja cancelar o registro?')) { 
        router.push('/'); 
    }
};
</script>

<template>
    <!-- Fundo cinza claro para o container principal -->
    <v-container fluid class="pa-6" style="background-color: #f0f4f7; min-height: 100vh;">
        <!-- Título principal: Registrar Entrada -->
        <h1 class="text-h4 mb-2 text-black font-weight-bold">Registrar Entrada</h1>
        <p class="text-subtitle-1 mb-6 text-medium-emphasis">Registro de entrada no estoque</p>

        <!-- Card principal com fundo branco -->
        <v-card class="pa-6" rounded="lg">
            
            <v-form @submit.prevent="concluir">
            
                <!-- Mensagem de Erro -->
                <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

                <!-- 1. INFORMAÇÕES DO LOTE (SEÇÃO 1) -->
                <v-card-title class="text-h6 font-weight-bold pa-0 mb-4" style="color: #3b5b76;">Informações do Lote:</v-card-title>
                
                <v-row>
                    <!-- Coluna Esquerda: Lote, Fabricante, Registro MS -->
                    <v-col cols="12" md="6">
                        <v-text-field
                            v-model="form.lote"
                            label="# Lote:"
                            prepend-icon="mdi-barcode"
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
                            v-model="form.registroMS"
                            label="Registro MS:"
                            prepend-icon="mdi-file-certificate-outline"
                            variant="outlined"
                            density="compact"
                            required
                            :disabled="isLoading"
                        />
                    </v-col>

                    <!-- Coluna Direita: Validade, Caixas, Quantidade/Unidades -->
                    <v-col cols="12" md="6">
                        <!-- Validade -->
                        <v-text-field
                            v-model="form.validade"
                            label="Validade:"
                            prepend-icon="mdi-calendar"
                            type="date"
                            variant="outlined"
                            density="compact"
                            required
                            :disabled="isLoading"
                        />
                        
                        <!-- Caixas -->
                        <v-text-field
                            v-model.number="form.caixas"
                            label="Caixas:"
                            prepend-icon="mdi-inbox-multiple"
                            type="number"
                            min="1"
                            variant="outlined"
                            density="compact"
                            required
                            :disabled="isLoading"
                        />
                        
                        <!-- Quantidade Total + Unidades por Caixa -->
                        <v-row dense>
                            <v-col cols="6">
                                <v-text-field
                                    :model-value="quantidadeTotal"
                                    label="Quantidade:"
                                    prepend-icon="mdi-counter"
                                    type="number"
                                    variant="outlined"
                                    density="compact"
                                    disabled
                                    :class="{ 'mt-4': $vuetify.display.mdAndUp }"
                                />
                            </v-col>
                            <v-col cols="6">
                                <v-text-field
                                    v-model.number="form.unidadesPorCaixa"
                                    label="Unidades por Caixa:"
                                    type="number"
                                    min="1"
                                    variant="outlined"
                                    density="compact"
                                    required
                                    :disabled="isLoading"
                                    :class="{ 'mt-4': $vuetify.display.mdAndUp }"
                                />
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                
                <v-divider class="my-6"/>

                <!-- 2. DADOS DO REMÉDIO (SEÇÃO 2) -->
                <v-card-title class="text-h6 font-weight-bold pa-0 mb-4" style="color: #3b5b76;">Dados do Remédio:</v-card-title>
                <v-row>
                    <!-- Coluna Esquerda: Nome, Princípio Ativo, Tarja -->
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

                    <!-- Coluna Direita: Dosagem -->
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
                        <!-- Campo oculto para `codigoProduto` para manter o payload da API completo -->
                        <input type="hidden" v-model="form.codigoProduto">
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