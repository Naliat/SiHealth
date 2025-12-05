<script lang="ts" setup>
import { ref } from 'vue';
const nomeUsuario = ref('Usuário');
const email = ref('usuario@dominio.com');
const senha = ref('');
const tamanhoFonte = ref('Média');
const showPassword = ref(false); 
const fontSizes = ['Pequena', 'Média', 'Grande'];
const isLoading = ref(false);
const showMessage = ref(false); 
const concluir = () => {
    isLoading.value = true;
    showMessage.value = false;
    
    console.log('Dados de Configuração Enviados:', {
        nomeUsuario: nomeUsuario.value,
        email: email.value,
        senha: senha.value,
        tamanhoFonte: tamanhoFonte.value,
    });
    
     setTimeout(() => {
        isLoading.value = false;
        showMessage.value = true;
        
        // Esconde a mensagem após 3 segundos
        setTimeout(() => {
            showMessage.value = false;
        }, 3000);
    }, 1500);
};
</script>

<template>
    <v-container fluid class="config-container">
        
        <v-alert
            v-if="showMessage"
            type="success"
            color="success"
            variant="tonal"
            border="start"
            title="Sucesso!"
            text="Configurações salvas com sucesso!"
            class="mb-4"
        />

        <h1 class="text-h4 mb-2">Configurações</h1>
        <p class="text-subtitle-1 mb-6 text-medium-emphasis">Configurações gerais do sistema</p>

        <v-card class="pa-6" rounded="lg">
            
            <v-card-title class="text-h6 font-weight-bold pa-0 mb-4">Geral:</v-card-title>
            
            <v-row>
                <v-col cols="12" md="8">
                    <v-text-field
                        v-model="nomeUsuario"
                        label="Nome do usuário:"
                        prepend-inner-icon="mdi-account"
                        variant="outlined"
                        density="compact"
                        :disabled="isLoading"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <v-select
                        v-model="tamanhoFonte"
                        :items="fontSizes"
                        label="Tamanho da fonte:"
                        variant="outlined"
                        density="compact"
                        :disabled="isLoading"
                        hide-details
                    />
                </v-col>
            </v-row>

            <v-row>
                <v-col cols="12" md="8">
                    <v-text-field
                        v-model="email"
                        label="E-mail:"
                        prepend-inner-icon="mdi-email"
                        variant="outlined"
                        density="compact"
                        :disabled="isLoading"
                    />
                </v-col>
                <v-col cols="12" md="4" /> 
            </v-row>
            
            <v-row>
                <v-col cols="12" md="8">
                    <v-text-field
                        v-model="senha"
                        label="Senha:"
                        prepend-inner-icon="mdi-lock"
                        :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="showPassword ? 'text' : 'password'"
                        @click:append-inner="showPassword = !showPassword"
                        variant="outlined"
                        density="compact"
                        hint="Deixe vazio para manter a senha atual"
                        persistent-hint
                        :disabled="isLoading"
                    />
                </v-col>
                <v-col cols="12" md="4" /> 
            </v-row>
            
            <div class="d-flex justify-end mt-4 pt-4">
                <v-btn 
                    color="#3b5b76" 
                    @click="concluir" 
                    :loading="isLoading"
                    :disabled="isLoading"
                >
                    Concluir
                </v-btn>
            </div>
        </v-card>
    </v-container>
</template>

<style scoped>
 .config-container {
    background-color: #e9eff3; 
    min-height: 100vh; 
    max-width: 100vw;
}

@media (max-width: 600px) {
    .config-container {
        padding: 8px !important;
        padding-top: 16px !important; 
    }

    .v-card {
        padding: 12px !important; 
    }
    
    .text-h4 {
        font-size: 1.75rem !important;
    }
}

.v-col {
    padding-bottom: 0;
}
</style>