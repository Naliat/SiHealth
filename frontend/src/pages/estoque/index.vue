<script lang="ts" setup>
import {reactive, ref, watch, onMounted} from 'vue'

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/lotes';
const API_MEDICAMENTO_URL = 'http://127.0.0.1:8000/api/v1/medicamentos';
const API_TIMEOUT = 5000;
const SYSTEM_SECRET_PASSWORD = import.meta.env.VITE_MASTER_PASSWORD || ''; 

interface MedicamentoDetalhe {
    id_medicamento: number;
    nome: string;
    principio_ativo: string;
    tarja: string;
    dosagem?: string; 
}

interface Lote {
    id_lote: number;
    numero_lote: string;
    numero_caixa: string;
    quantidade_por_caixa: number;
    quantidade_inicial: number;
    data_fabricacao: string;
    data_validade: string;
    id_medicamento: number;
    quantidade_atual: number;
    criado_em: string; 
    status: 'OK' | 'Próx. Venc.' | 'Vencido';
    medicamento: MedicamentoDetalhe; 
    nome_medicamento?: string; 
}

interface DataTableOptions {
    itemsPerPage: number;
    sortBy: { key: string; order: string; }[];
    search?: string; 
    page: number; 
    [key: string]: any; 
}

const state = reactive({
  search: '',
  displaySort: 'Data Vencimento' as 'Alfabética' | 'Data Vencimento' | 'Quantidade',
  expanded: {} as Record<number, boolean>,
})

const items = ref<Lote[]>([]);
const loading = ref(false);
const totalItems = ref(0);

const MAX_ITEMS_PER_PAGE = 500;
const itemsPerPageOptions = [
    { value: 10, title: '10' },
    { value: 50, title: '50' },
    { value: 100, title: '100' },
    { value: MAX_ITEMS_PER_PAGE, title: 'Todos' }
];

const options = ref<DataTableOptions>({
    itemsPerPage: MAX_ITEMS_PER_PAGE, 
    sortBy: [{key: 'validade', order: 'asc'}], 
    page: 1,
    search: '',
});

const localFallback = ref([
  {
    numero_lote: 'DEV-0001',
    numero_caixa: '1',
    quantidade_por_caixa: 12,
    quantidade_inicial: 12,
    data_fabricacao: '2025-11-28',
    data_validade: '2099-12-31',
    id_lote: 1,
    id_medicamento: 1001,
    quantidade_atual: 12,
    criado_em: '2025-11-28T13:34:45.422Z',
    status: 'OK',
    medicamento: { id_medicamento: 1001, nome: 'Paracetamol - Teste', principio_ativo: 'Acetaminofeno', tarja: 'Livre' } 
  },
  {
    numero_lote: 'DEV-0002',
    numero_caixa: '0',
    quantidade_por_caixa: 12,
    quantidade_inicial: 24,
    data_fabricacao: '2025-11-28',
    data_validade: '2024-12-31',
    id_lote: 2,
    id_medicamento: 1002,
    quantidade_atual: 0,
    criado_em: '2025-11-28T13:34:45.422Z',
    status: 'Próx. Venc.',
    medicamento: { id_medicamento: 1002, nome: 'Amoxicilina - Teste', principio_ativo: 'Amoxicilina', tarja: 'Vermelha' } 
  },
])


const getStatusClass = (status: string) => {
  switch (status) {
    case 'OK':
      return 'status-ok'
    case 'Próx. Venc.':
      return 'status-warning'
    case 'Vencido':
      return 'status-expired'
    default:
      return ''
  }
}

const toggleRow = (idLote: number) => {
  state.expanded[idLote] = !state.expanded[idLote]
}
const isExpanded = (idLote: number) => state.expanded[idLote]


const showEntryDialog = ref(false) 
const showConfirmPasswordDialog = ref(false) 
const isEntrySubmitting = ref(false)
const showSnackbar = ref(false) 
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const loteNumero = ref('')
const loteFabricante = ref('')
const loteRegistroMS = ref('')
const loteValidade = ref(new Date().toISOString().substring(0, 10))
const loteCaixas = ref(1)
const loteQuantidadeUnidades = ref(1)

const medicamentoOptions = ref<MedicamentoDetalhe[]>([]); 
const nomeMedicamentoSearch = ref(''); 
const medicamentoSelecionadoObjeto = ref<MedicamentoDetalhe | null>(null); 

const idMedicamentoSelecionado = ref<number | null>(null); 
const remedioPrincipioAtivo = ref('');
const remedioDosagem = ref('');
const remedioTarja = ref('');
const tarjasOpcoes = ['Livre', 'Amarela', 'Vermelha', 'Preta'];


const masterPassword = ref('')
const masterPasswordError = ref(false)


const resetForm = () => {
    loteNumero.value = ''
    loteFabricante.value = ''
    loteRegistroMS.value = ''
    loteValidade.value = new Date().toISOString().substring(0, 10)
    loteCaixas.value = 1
    loteQuantidadeUnidades.value = 1
    
    medicamentoSelecionadoObjeto.value = null;
    idMedicamentoSelecionado.value = null;
    nomeMedicamentoSearch.value = '';
    remedioPrincipioAtivo.value = '';
    remedioDosagem.value = '';
    remedioTarja.value = '';
    
    masterPassword.value = ''
    masterPasswordError.value = false
}

let searchMedTimeout: ReturnType<typeof setTimeout>;
const searchMedicamentos = async (query: string) => {
    const q = query.trim();

    clearTimeout(searchMedTimeout);
    searchMedTimeout = setTimeout(async () => {
        const params = new URLSearchParams();
        if (q) params.append('nome', q);
        params.append('limit', '10');

        try {
            const url = `${API_MEDICAMENTO_URL}?${params.toString()}`;
            console.log('Searching Meds:', url);
            const response = await fetch(url, { signal: AbortSignal.timeout(API_TIMEOUT) });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data: MedicamentoDetalhe[] = await response.json();
            medicamentoOptions.value = data;

        } catch (error) {
            console.error('Erro ao buscar medicamentos:', error);
            medicamentoOptions.value = [];
        }
    }, q.length > 0 ? 300 : 0);
};

const handleOpenAutocomplete = () => {
    if (medicamentoOptions.value.length === 0 && !medicamentoSelecionadoObjeto.value) {
        searchMedicamentos('');
    }
};


watch(medicamentoSelecionadoObjeto, (newObj) => {
    if (newObj && newObj.id_medicamento) {
        idMedicamentoSelecionado.value = newObj.id_medicamento;
        remedioPrincipioAtivo.value = newObj.principio_ativo || '';
        remedioDosagem.value = newObj.dosagem || '';
        remedioTarja.value = newObj.tarja || '';
    } else {
        idMedicamentoSelecionado.value = null;
        remedioPrincipioAtivo.value = '';
        remedioDosagem.value = '';
        remedioTarja.value = '';
    }
});


const fetchItems = async () => {
    loading.value = true;
    
    const params = new URLSearchParams();
    
    const limit = options.value.itemsPerPage || MAX_ITEMS_PER_PAGE;
    const skip = (options.value.page - 1) * limit;

    params.append('skip', String(skip));
    params.append('limit', String(limit));
    
    if (options.value.search) { 
        params.append('numero_lote', options.value.search);
        params.append('medicamento', options.value.search); 
    }

    const sortBy = options.value.sortBy?.[0]?.key || 'validade';
    const sortDirection = options.value.sortBy?.[0]?.order || 'asc';
    
    params.append('ordenar_por', sortBy);
    params.append('direcao', sortDirection);

    try {
        const url = `${API_BASE_URL}?${params.toString()}`;
        console.log('Fetching Lotes:', url); 
        
        const response = await fetch(url, { signal: AbortSignal.timeout(API_TIMEOUT) });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data: Lote[] = await response.json();
        
        items.value = data;
        totalItems.value = data.length; 
        
        if (data.length > 0) {
            console.log('ESTRUTURA DE DADOS RECEBIDA (VERIFIQUE medicamento.nome):', data[0]);
        }

    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        snackbarColor.value = 'error';
        snackbarMessage.value = 'Erro ao carregar dados. Verifique o backend.';
        showSnackbar.value = true;
        
        items.value = localFallback.value as Lote[];
        totalItems.value = localFallback.value.length;
    } finally {
        loading.value = false;
    }
}


interface LoteCreate {
    id_medicamento: number; 
    numero_lote: string;
    data_fabricacao: string;
    data_validade: string;
    quantidade_por_caixa: number;
    quantidade_inicial: number;
    numero_caixa: string;
}

const criarLote = async (masterPass: string) => {
    
    if (idMedicamentoSelecionado.value === null) {
         return { success: false, message: 'Selecione um medicamento válido.' };
    }
    
    const payload: LoteCreate = {
        id_medicamento: idMedicamentoSelecionado.value, 
        numero_lote: loteNumero.value,
        data_fabricacao: new Date().toISOString().substring(0, 10), 
        data_validade: loteValidade.value,
        quantidade_por_caixa: loteQuantidadeUnidades.value,
        quantidade_inicial: loteCaixas.value * loteQuantidadeUnidades.value,
        numero_caixa: String(loteCaixas.value),
    };

    try {
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Admin-Pass': masterPass, 
            },
            body: JSON.stringify(payload),
            signal: AbortSignal.timeout(API_TIMEOUT),
        });

        if (response.status === 401 || response.status === 403) {
            return { success: false, message: 'Falha na autenticação: Senha-mestre rejeitada.' };
        }
        
        if (!response.ok) {
            const errorBody = await response.json();
            console.error("Backend Error:", errorBody);
            return { success: false, message: `Erro ao criar lote: ${errorBody.detail || response.statusText}` };
        }

        return { success: true, message: 'Nova entrada cadastrada com sucesso!' };

    } catch (error) {
        console.error('Erro ao criar lote:', error);
        return { success: false, message: 'Erro de rede ou servidor ao cadastrar.' };
    }
};


const handleConcluirEntrada = () => {
    if (idMedicamentoSelecionado.value === null || loteNumero.value === '') {
        snackbarColor.value = 'warning';
        snackbarMessage.value = 'Preencha o Lote e selecione um Medicamento válido.';
        showSnackbar.value = true;
        return;
    }
    
    showConfirmPasswordDialog.value = true;
    masterPassword.value = '';
    masterPasswordError.value = false;
}

const confirmarESalvarEntrada = async () => {
    masterPasswordError.value = false;
    isEntrySubmitting.value = true
    
    const trimmedPassword = masterPassword.value.trim();
    
    if (!trimmedPassword) {
        masterPasswordError.value = true;
        snackbarColor.value = 'error';
        snackbarMessage.value = 'A senha não pode estar vazia.';
        showSnackbar.value = true;
        isEntrySubmitting.value = false;
        return;
    }
    
    const result = await criarLote(trimmedPassword);
    
    isEntrySubmitting.value = false
    showConfirmPasswordDialog.value = false 
    showEntryDialog.value = false  

    if (result.success) {
        snackbarColor.value = 'success';
        snackbarMessage.value = result.message;
        resetForm();
        
        options.value = { ...options.value, page: 1 };
        
    } else {
        snackbarColor.value = 'error';
        snackbarMessage.value = result.message;
        
        showEntryDialog.value = true; 
        showConfirmPasswordDialog.value = true; 
    }
    showSnackbar.value = true;
}

const cancelarEntrada = () => {
    showEntryDialog.value = false;
    resetForm();
}

const cancelarConfirmacao = () => {
    showConfirmPasswordDialog.value = false;
    masterPassword.value = '';
    masterPasswordError.value = false;
}

let searchTimeout: ReturnType<typeof setTimeout>

watch(
  () => state.search,
  (newVal) => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      options.value = {...options.value, search: newVal, page: 1}
    }, 500)
  }
)

watch(
  () => options.value.sortBy,
  (newSort) => {
    if (!newSort || newSort.length === 0) return;
    
    const key = newSort[0].key;
    const order = newSort[0].order;
    
    if (key === 'validade' && order === 'asc') state.displaySort = 'Data Vencimento';
    else if (key === 'quantidade' && order === 'desc') state.displaySort = 'Quantidade';
    else if (key === 'medicamento' && order === 'asc') state.displaySort = 'Alfabética'; 
    else state.displaySort = 'Data Vencimento'; 
  },
  { deep: true, immediate: true }
);


watch([options], () => {
    fetchItems();
}, { deep: true, immediate: true }); 

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
                    @keydown.enter="confirmarESalvarEntrada"
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
                    @click="confirmarESalvarEntrada"
                    :loading="isEntrySubmitting"
                    :disabled="isEntrySubmitting"
                >
                    Concluir
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    
    <v-dialog v-model="showEntryDialog" max-width="800px" transition="slide-y-transition">
        <v-card class="modal-card" rounded="xl" elevation="10">
            <v-card-title class="text-h5 font-weight-bold text-center pa-6">
                Registrar Entrada
            </v-card-title>
            <p class="text-center text-subtitle-1 text-slate-600 mb-4">Registro de entrada no estoque</p>
            
         
            <v-card-text class="pa-6">
                <v-card class="pa-6 form-box mb-6" rounded="lg" elevation="1">
                    <v-card-title class="text-h6 font-weight-bold pa-0 mb-4">
                        Informações do Lote:
                    </v-card-title>
                    <v-row>
                        <v-col cols="12" md="4">
                            <v-text-field
                                v-model="loteNumero"
                                label="# Lote:"
                                prepend-inner-icon="mdi-pound"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                            />
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-text-field
                                v-model="loteFabricante"
                                label="Fabricante:"
                                prepend-inner-icon="mdi-factory"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                            />
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-text-field
                                v-model="loteRegistroMS"
                                label="Registro MS:"
                                prepend-inner-icon="mdi-id-card"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                            />
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12" md="4">
                            <v-text-field
                                v-model="loteValidade"
                                label="Validade:"
                                prepend-inner-icon="mdi-calendar"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                                type="date"
                            />
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-text-field
                                v-model.number="loteCaixas"
                                label="Caixas:"
                                prepend-inner-icon="mdi-package-variant"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                                type="number"
                                min="1"
                            />
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-text-field
                                v-model.number="loteQuantidadeUnidades"
                                label="Unidades por Caixa:"
                                prepend-inner-icon="mdi-cube-outline"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                                type="number"
                                min="1"
                            />
                        </v-col>
                    </v-row>
                </v-card>
                
                <v-card class="pa-6 form-box" rounded="lg" elevation="1">
                    <v-card-title class="text-h6 font-weight-bold pa-0 mb-4">
                        Dados do Remédio:
                    </v-card-title>
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-autocomplete
                                v-model="medicamentoSelecionadoObjeto"
                                @update:search="searchMedicamentos"
                                @click:append-inner="handleOpenAutocomplete"
                                :items="medicamentoOptions"
                                item-title="nome"
                                item-value="id_medicamento"
                                label="Nome do remédio:"
                                placeholder="Digite o nome para buscar..."
                                prepend-inner-icon="mdi-pill"
                                append-inner-icon="mdi-menu-down"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                                :loading="false"
                                return-object
                                clearable
                            />
                        </v-col>
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="remedioPrincipioAtivo"
                                label="Princípio Ativo:"
                                prepend-inner-icon="mdi-flask"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                                :disabled="true" 
                            />
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12" md="4">
                             <v-select
                                v-model="remedioTarja"
                                :items="tarjasOpcoes"
                                label="Tarja:"
                                prepend-inner-icon="mdi-lock"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                                hide-details
                                :disabled="true"
                            />
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-text-field
                                v-model="remedioDosagem"
                                label="Dosagem (mg/ml):"
                                prepend-inner-icon="mdi-scale-balance"
                                variant="outlined"
                                density="comfortable"
                                rounded="lg"
                                :disabled="true"
                            />
                        </v-col>
                        <v-col cols="12" md="4"></v-col>
                    </v-row>
                </v-card>
            </v-card-text>
            
            <!-- Ações do Pop-up -->
            <v-card-actions class="pa-6 d-flex justify-space-between">
                <v-btn
                    class="modal-btn-cancel"
                    color="#c25353"
                    variant="flat"
                    size="large"
                    rounded="lg"
                    @click="cancelarEntrada"
                    :disabled="isEntrySubmitting"
                >
                    Cancelar
                </v-btn>
                <v-btn
                    class="modal-btn-confirm"
                    color="#3b5b76"
                    variant="flat"
                    size="large"
                    rounded="lg"
                    @click="handleConcluirEntrada"
                    :loading="isEntrySubmitting"
                    :disabled="isEntrySubmitting"
                >
                    Concluir
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <!-- FIM DO POP-UP -->


    <div class="d-flex justify-space-between align-start mb-8">
      <div>
        <h1 class="text-h3 font-weight-bold text-slate-900 mb-2">Lista do Estoque</h1>
        <p class="text-h6 text-slate-600">Visão geral da lista do estoque</p>
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
        v-model="state.search"
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
              {{ state.displaySort }}
              <v-icon end size="small">mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="options.sortBy = [{key: 'medicamento', order: 'asc'}]">
              <v-list-item-title>Alfabética</v-list-item-title>
            </v-list-item>
            <v-list-item @click="options.sortBy = [{key: 'validade', order: 'asc'}]">
              <v-list-item-title>Data Vencimento</v-list-item-title>
            </v-list-item>
            <v-list-item @click="options.sortBy = [{key: 'quantidade', order: 'desc'}]">
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
        no-data-text="Nenhum item de estoque encontrado."
        :items-per-page-options="itemsPerPageOptions" 
      >

        <template #headers>
          <tr class="table-header-row">
            <th class="text-center pa-4" style="width: 10%; max-width: 10%;">
              <div class="d-flex align-center justify-center ga-2">
                <span class="header-icon">#</span>
                <span class="header-text">Número</span>
              </div>
            </th>
            <th class="text-left pa-4" style="width: 50%; max-width: 50%;">
              <div class="d-flex align-center ga-2">
                <span class="header-icon">Tt</span>
                <span class="header-text">Nome do remédio</span>
              </div>
            </th>
            <th class="pa-4" style="width: 2%; max-width: 2%"></th>
            <th class="text-center pa-4" style="width: 19%; max-width: 19%;">
              <div class="d-flex align-center justify-center ga-2">
                <span class="header-icon"><v-icon>mdi-check-circle-outline</v-icon></span>
                <span class="header-text">Status</span>
              </div>
            </th>
            <th class="text-center pa-4" style="width: 19%; max-width: 19%;">
              <div class="d-flex align-center justify-center ga-2">
                <span class="header-icon">⋮⋮</span>
                <span class="header-text">Ações</span>
              </div>
            </th>
          </tr>
        </template>

        <template #item="{ item }">

          <tr class="table-row">
            <td class="text-center pa-5">
              <div class="number-badge">
                {{ item.id_lote ?? item.id_medicamento ?? '-' }}
              </div>
            </td>

            <td class="text-left pa-5">
              <div class="d-flex align-center">
                <div class="vertical-divider"></div>
                <span class="medicine-name">{{ item.medicamento?.nome ?? item.numero_lote ?? '-' }}</span>
              </div>
            </td>

            <td class="pa-5"></td>

            <td class="text-center pa-5">
              <v-chip
                :class="getStatusClass(item.status ?? '')"
                class="status-chip"
                size="small"
              >
                {{ item.status ?? '—' }}
              </v-chip>
            </td>

            <td class="text-center pa-5">
              <v-btn
                class="action-btn"
                icon
                size="small"
                @click="toggleRow(item.id_lote)"
              >
                <v-icon size="20">{{ isExpanded(item.id_lote) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </td>
          </tr>

          <tr v-if="isExpanded(item.id_lote)">
            <td class="pa-0" colspan="5">
              <div class="expanded-card">
                <div class="expanded-section">
                  <h3 class="expanded-title">Informações Básicas:</h3>
                  <div class="expanded-grid">
                    <div class="expanded-item">
                      <span class="label"><v-icon class="me-1" size="18">mdi-pound</v-icon> Código do Produto:</span>
                      <span class="value">{{ item.id_medicamento ?? '-' }}</span>
                    </div>
                    <div class="expanded-item">
                      <span class="label"><v-icon class="me-1" size="18">mdi-package-variant</v-icon> Caixas:</span>
                      <span class="value">{{ item.numero_caixa ?? '-' }} Unidades </span>
                    </div>
                    <div class="expanded-item">
                      <span class="label"><v-icon class="me-1" size="18">mdi-cube</v-icon> Unidades/caixa:</span>
                      <span class="value">{{ item.quantidade_por_caixa ?? '-' }}</span>
                    </div>
                  </div>
                </div>

                <div class="expanded-section">
                  <h3 class="expanded-title">Informações do Fabricante:</h3>
                  <div class="expanded-grid">
                    <div class="expanded-item">
                      <span class="label"><v-icon class="me-1" size="18">mdi-pound</v-icon> Lote:</span>
                      <span class="value">{{ item.numero_lote ?? '-' }}</span>
                    </div>
                    <div class="expanded-item">
                      <span class="label"><v-icon class="me-1" size="18">mdi-calendar</v-icon> Validade:</span>
                      <span class="value">{{ item.data_validade ? new Date(item.data_validade).toLocaleDateString() : '-' }}</span>
                    </div>
                  </div>
                </div>

                <div class="expanded-actions">
                  <v-btn color="primary" icon variant="tonal">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn color="error" icon variant="tonal">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </div>
              </div>
            </td>
          </tr>
        </template>

        <template #body.append>
          <tr>
            <td class="table-footer pa-6" colspan="5">
              <div class="d-flex justify-end">
                <v-btn
                  class="report-btn"
                  color="primary"
                  rounded="lg"
                  size="large"
                  variant="flat"
                  @click="showEntryDialog = true"
                >
                  + Cadastrar nova entrada
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

/* 📱 AJUSTES DE RESPONSIVIDADE DO MODAL */
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


/* --- ESTILOS EXISTENTES DA LISTA --- */
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

.status-chip {
  font-weight: 500 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  border-radius: 16px !important;
  padding: 0 16px !important;
  height: 28px !important;
  border: 1px solid !important;
}

.status-ok {
  background-color: #d1fae5 !important;
  color: #059669 !important;
  border-color: #a7f3d0 !important;
}

.status-warning {
  background-color: #fef3c7 !important;
  color: #d97706 !important;
  border-color: #fde68a !important;
}

.status-expired {
  background-color: #fee2e2 !important;
  color: #dc2626 !important;
  border-color: #fecaca !important;
}

.action-btn {
  background-color: #475569 !important;
  color: white !important;
  border-radius: 50% !important;
  width: 40px !important;
  height: 40px !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-btn:hover {
  background-color: #334155 !important;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
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

.expanded-card {
  display: flex;
  gap: 32px;
  padding: 24px 32px;
  background-color: #e5edf5;
  border-left: 1px solid #e2e8f0;
  border-right: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  border-radius: 0 0 24px 24px;
}

.expanded-section {
  flex: 1;
}

.expanded-title {
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 12px;
}

.expanded-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 24px;
}

.expanded-item .label {
  font-weight: 600;
  font-size: 0.85rem;
}

.expanded-item .value {
  margin-left: 4px;
  font-size: 0.85rem;
}

.expanded-actions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 12px;
  padding-left: 24px;
  border-left: 1px solid #cbd5e1;
}
</style>