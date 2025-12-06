<script lang="ts" setup>
import { ref, watch } from 'vue'
interface DataTableOptions {
    itemsPerPage: number;
    sortBy: { key: string; order: string; }[];
    search?: string; 
    page: number;
    [key: string]: any;
}
const search = ref('')
const displaySort = ref('Alfabética')

const items = ref([
    { id_medicamento: 1, nome: 'Paracetamol', principio_ativo: 'Acetaminofeno', tarja: 'Vermelha' },
    { id_medicamento: 2, nome: 'Amoxicilina', principio_ativo: 'Amoxicilina tri-hidratada', tarja: 'Amarela' },
    { id_medicamento: 3, nome: 'Dorflex', principio_ativo: 'Dipirona, Orfenadrina', tarja: 'Livre' },
]);
const loading = ref(false);
const totalItems = ref(3);
const options = ref<DataTableOptions>({
    itemsPerPage: 10,
    sortBy: [{ key: 'nome', order: 'asc' }],
    page: 1,
    search: '', 
});


let searchTimeout: ReturnType<typeof setTimeout>

watch(search, (newVal) => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    
    options.value = { ...options.value, search: newVal, page: 1 }
  }, 500)
})


const showRegisterDialog = ref(false)
const showConfirmPasswordDialog = ref(false) 
const isSubmitting = ref(false)
const showSnackbar = ref(false)
const snackbarMessage = ref('Remédio cadastrado com sucesso!')
const snackbarColor = ref('success')
const nomeRemedio = ref('')
const principioAtivo = ref('')
const tarja = ref('Livre')
const tarjasOpcoes = ['Livre', 'Amarela', 'Vermelha', 'Preta']
const masterPassword = ref('')
const masterPasswordError = ref(false)
const SIMULATED_MASTER_PASSWORD = '123' 

const resetForm = () => {
    nomeRemedio.value = ''
    principioAtivo.value = ''
    tarja.value = 'Livre'
    masterPassword.value = ''
    masterPasswordError.value = false
}

const handleConcluirRegistro = () => {
    showConfirmPasswordDialog.value = true;
}

const confirmarESalvar = () => {
    masterPasswordError.value = false;
    
    if (masterPassword.value !== SIMULATED_MASTER_PASSWORD) {
        masterPasswordError.value = true;
        snackbarColor.value = 'error';
        snackbarMessage.value = 'Senha-mestre incorreta. Tente novamente.';
        showSnackbar.value = true;
        return;
    }

    isSubmitting.value = true
    showConfirmPasswordDialog.value = false 
    showRegisterDialog.value = false 
    
    
    console.log('Novo Remédio Registrado APÓS CONFIRMAÇÃO:', {
        nomeRemedio: nomeRemedio.value,
        principioAtivo: principioAtivo.value,
        tarja: tarja.value,
    })

    setTimeout(() => {
        isSubmitting.value = false
        
       
        snackbarColor.value = 'success';
        snackbarMessage.value = 'Remédio cadastrado com sucesso!';
        showSnackbar.value = true
        resetForm() 
    }, 1500)
}

const cancelarCadastro = () => {
    showRegisterDialog.value = false;
    resetForm();
}

const cancelarConfirmacao = () => {
    showConfirmPasswordDialog.value = false;
    masterPassword.value = '';
    masterPasswordError.value = false;
}
</script>

<template>
  <v-container class="page-container pa-8 bg-gradient" fluid>
    
   
    <v-snackbar
        v-model="showSnackbar"
        :color="snackbarColor"
        timeout="3000"
        location="top right"
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
        transition="slide-y-transition"
        persistent
    >
        <v-card class="modal-card pa-6" rounded="xl" elevation="10">
            <v-card-title class="text-h4 font-weight-bold text-center pa-0 mb-4">
                Confirmação
            </v-card-title>
            <p class="text-h6 text-slate-600 text-center mb-6">Confirme colocando a senha-mestre</p>
            
            <v-card-text>
                <v-text-field
                    v-model="masterPassword"
                    label="Senha-mestre"
                    prepend-inner-icon="mdi-lock"
                    :type="'password'"
                    variant="outlined"
                    density="comfortable"
                    rounded="lg"
                    :error="masterPasswordError"
                    :error-messages="masterPasswordError ? 'Senha incorreta.' : ''"
                    @keydown.enter="confirmarESalvar"
                />
            </v-card-text>
            
            <v-card-actions class="pa-0 d-flex justify-space-between">
                <v-btn
                    class="modal-btn-cancel"
                    color="#c25353"
                    variant="flat"
                    size="large"
                    rounded="lg"
                    @click="cancelarConfirmacao"
                >
                    Cancelar
                </v-btn>
                <v-btn
                    class="modal-btn-confirm"
                    color="#3b5b76"
                    variant="flat"
                    size="large"
                    rounded="lg"
                    @click="confirmarESalvar"
                    :loading="isSubmitting"
                    :disabled="isSubmitting"
                >
                    Concluir
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-dialog v-model="showRegisterDialog" max-width="500px" transition="slide-y-transition">
        <v-card class="modal-card" rounded="xl" elevation="10">
            <v-card-title class="text-h5 font-weight-bold text-center pa-6">
                Registrar Remédio
            </v-card-title>
            <p class="text-center text-subtitle-1 text-slate-600 mb-4">Registro de novo remédio</p>
            
           
            <v-card-text class="pa-6">
                <v-card class="pa-6 form-box" rounded="lg" elevation="1">
                    <v-card-title class="text-center text-h6 font-weight-bold pa-0 mb-4">
                        Dados do Remédio:
                    </v-card-title>
                    
                    <v-text-field
                        v-model="nomeRemedio"
                        label="Nome do remédio:"
                        prepend-inner-icon="mdi-pill"
                        variant="outlined"
                        density="comfortable"
                        rounded="lg"
                    />

                    <v-text-field
                        v-model="principioAtivo"
                        label="Princípio Ativo:"
                        prepend-inner-icon="mdi-flask"
                        variant="outlined"
                        density="comfortable"
                        rounded="lg"
                    />
                    
                    <v-select
                        v-model="tarja"
                        :items="tarjasOpcoes"
                        label="Tarja:"
                        prepend-inner-icon="mdi-lock"
                        variant="outlined"
                        density="comfortable"
                        rounded="lg"
                        hide-details
                    />
                </v-card>
            </v-card-text>
            
            <v-card-actions class="pa-6 d-flex justify-space-between">
                <v-btn
                    class="modal-btn-cancel"
                    color="#c25353"
                    variant="flat"
                    size="large"
                    rounded="lg"
                    @click="cancelarCadastro"
                    :disabled="isSubmitting"
                >
                    Cancelar
                </v-btn>
                <v-btn
                    class="modal-btn-confirm"
                    color="#3b5b76"
                    variant="flat"
                    size="large"
                    rounded="lg"
                    @click="handleConcluirRegistro"
                    :loading="isSubmitting"
                    :disabled="isSubmitting"
                >
                    Concluir
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>


    <div class="d-flex justify-space-between align-start mb-8">
      <div>
        <h1 class="text-h3 font-weight-bold text-slate-900 mb-2">Lista de Remédios</h1>
        <p class="text-h6 text-slate-600">Visão geral da lista de remédios</p>
      </div>
      <v-btn class="user-btn" variant="text">
        <v-icon start>mdi-account-circle</v-icon>
        Usuário
        <v-icon end size="small">mdi-chevron-down</v-icon>
      </v-btn>
    </div>

    <v-progress-linear
      v-if="loading"
      class="mb-4"
      color="primary"
      indeterminate
      rounded
    />

    <div class="d-flex justify-space-between align-center mb-6">
      <v-text-field
        v-model="search"
        class="search-field"
        density="comfortable"
        hide-details
        placeholder="Buscar remédio..."
        prepend-inner-icon="mdi-magnify"
        style="max-width: 400px;"
        variant="outlined"
      />

      <div class="d-flex align-center ga-2">
        <span class="text-body-2 text-slate-600">sort:</span>
        <v-menu offset-y>
          <template #activator="{ props }">
            <v-btn class="sort-btn" size="small" v-bind="props" variant="outlined">
              {{ displaySort }}
              <v-icon end size="small">mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="displaySort = 'Alfabética'">
              <v-list-item-title>Alfabética</v-list-item-title>
            </v-list-item>
            <v-list-item @click="displaySort = 'Data Vencimento'">
              <v-list-item-title>Data Vencimento</v-list-item-title>
            </v-list-item>
            <v-list-item @click="displaySort = 'Quantidade'">
              <v-list-item-title>Quantidade</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>

    <v-card class="table-card" elevation="3" rounded="xl">
      <v-data-table-server
        v-model:options="options"
        :items="items"
        :items-length="totalItems"
        :loading="loading"
        class="custom-table"
        hide-default-footer
        no-data-text="Nenhum remédio encontrado."
      >

        <template #headers>
          <tr class="table-header-row">
            <th class="text-center pa-4" style="width: 10%; max-width: 10%;">
              <div class="d-flex align-center justify-center ga-2">
                <span class="header-icon">#</span>
                <span class="header-text">Número</span>
              </div>
            </th>
            <th class="text-left pa-4" style="width: 90%; max-width: 90%;">
              <div class="d-flex align-center ga-2">
                <span class="header-icon">Tt</span>
                <span class="header-text">Nome do remédio</span>
              </div>
            </th>
          </tr>
        </template>

        <template #item="{ item }">
          <tr class="table-row">
            <td class="text-center pa-5">
              <div class="number-badge">
                {{ item.id_medicamento }}
              </div>
            </td>

            <td class="text-left pa-5">
              <div class="d-flex align-center">
                <div class="vertical-divider"></div>
                <span class="medicine-name">{{ item.nome ?? '-' }}</span>
              </div>
            </td>
          </tr>
        </template>

        <template #body.append>
          <tr>
            <td class="table-footer pa-6" colspan="2">
              <div class="d-flex justify-end">
                <v-btn
                  class="report-btn"
                  color="primary"
                  rounded="lg"
                  size="large"
                  variant="flat"
                  @click="showRegisterDialog = true"
                >
                  + Registrar novo remédio 
                </v-btn>
              </div>
            </td>
          </tr>
        </template>
      </v-data-table-server>
    </v-card>
  </v-container>
</template>

<style scoped>


.modal-card {
    background-color: #e9eff3;
    border: 3px solid #cbd5e1;
    overflow: hidden;
}

.form-box {
    background-color: white;
    border: 1px solid #e2e8f0;
}

.modal-btn-cancel {
    color: white !important;
    text-transform: none !important;
    letter-spacing: normal !important;
}

.modal-btn-confirm {
    color: white !important;
    text-transform: none !important;
    letter-spacing: normal !important;
}

@media (max-width: 550px) {
    .modal-card {
        margin: 16px !important;
    }
    .v-card-actions {
        flex-direction: column;
    }
    .modal-btn-cancel, .modal-btn-confirm {
        width: 100%;
        margin-top: 8px;
    }
}
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

.user-btn {
  color: #475569 !important;
  text-transform: none;
  letter-spacing: normal;
}

.user-btn:hover {
  background-color: rgba(148, 163, 184, 0.1) !important;
}

.search-field :deep(.v-field) {
  background-color: white;
  border-radius: 12px;
}

.search-field :deep(.v-field__outline) {
  --v-field-border-opacity: 0.2;
}

.search-field :deep(.v-field:hover .v-field__outline) {
  --v-field-border-opacity: 0.3;
}

.search-field :deep(.v-field--focused .v-field__outline) {
  --v-field-border-opacity: 1;
}

.sort-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
  color: #475569 !important;
  border-color: #cbd5e1 !important;
}

.table-card {
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.custom-table {
  background-color: transparent;
}

.custom-table :deep(.v-table__wrapper) {
  border-radius: 0;
}

.custom-table :deep(table) {
  border-collapse: separate;
}

.table-header-row {
  background-color: #f8fafc !important;
  border-bottom: 1px solid #e2e8f0;
}

.table-header-row th {
  font-weight: 600 !important;
  color: #64748b !important;
  font-size: 0.875rem !important;
  border-bottom: none !important;
  background-color: #f8fafc !important;
  height: 60px !important;
}

.header-icon {
  font-size: 1.125rem;
  color: #64748b;
}

.header-text {
  font-weight: 500;
  color: #64748b;
}

.table-row {
  transition: background-color 0.2s ease;
}

.table-row:hover {
  background-color: #f8fafc !important;
}

.table-row td {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-left: none;
  border-right: none;
  vertical-align: middle;
  padding: 18px 16px;
}

.table-row td:first-child {
  border-left: 1px solid #e2e8f0;
  border-top-left-radius: 24px;
  border-bottom-left-radius: 24px;
}

.table-row td:last-child {
  border-right: 1px solid #e2e8f0;
  border-top-right-radius: 24px;
  border-bottom-right-radius: 24px;
}

.number-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background-color: #f1f5f9;
  border-radius: 50%;
  font-weight: 600;
  font-size: 0.875rem;
  color: #475569;
}

.vertical-divider {
  width: 4px;
  height: 32px;
  background-color: #e2e8f0;
  border-radius: 2px;
  margin-right: 20px;
}

.medicine-name {
  font-size: 1rem;
  font-weight: 500;
  color: #0f172a;
}

.table-footer {
  background-color: #f8fafc !important;
  border-top: 1px solid #e2e8f0 !important;
}

.report-btn {
  background-color: #475569 !important;
  color: white !important;
  text-transform: none !important;
  letter-spacing: normal !important;
  font-weight: 500 !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.report-btn:hover {
  background-color: #334155 !important;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}
</style>