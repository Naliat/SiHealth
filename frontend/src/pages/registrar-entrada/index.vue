<script lang="ts" setup>
import { ref, reactive } from 'vue';

const form = reactive({
  codigo: '',
  nome: '',
  principioAtivo: '',
  tarja: null,
  caixas: 1,
  qtdPorCaixa: 1,
  dosagem: '',
  dosagemUnidade: 'mg',
  lote: '',
  validade: '',
  fabricante: '',
  registroMs: ''
});

const tarjaOptions = ['Sem Tarja', 'Tarja Amarela', 'Tarja Vermelha', 'Tarja Preta'];
const unidadeOptions = ['mg', 'g', 'ml', 'mcg'];

const updateNumber = (field: 'caixas' | 'qtdPorCaixa', delta: number) => {
  const newValue = form[field] + delta;
  if (newValue >= 1) {
    form[field] = newValue;
  }
};

const submitForm = () => {
  console.log('Formulário enviado:', form);
};
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

      <v-card class="mb-6 pa-6" elevation="3" rounded="xl">
        <h2 class="section-title mb-6">Dados do Remédio:</h2>

        <v-row dense>
          <v-col cols="12" md="8">
            <div class="mb-4">
              <label class="input-label"># Código do Produto:</label>
              <v-text-field
                v-model="form.codigo"
                placeholder="Digite o código"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
              ></v-text-field>
            </div>

            <div class="mb-4">
              <label class="input-label"><v-icon icon="mdi-pill" size="small" class="mr-1"/> Nome do remédio:</label>
              <v-text-field
                v-model="form.nome"
                placeholder="Digite o nome"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
              ></v-text-field>
            </div>

            <div class="mb-4">
              <label class="input-label"><v-icon icon="mdi-flask" size="small" class="mr-1"/> Princípio Ativo:</label>
              <v-text-field
                v-model="form.principioAtivo"
                placeholder="Digite o princípio ativo"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
              ></v-text-field>
            </div>

            <div>
              <label class="input-label"><v-icon icon="mdi-lock" size="small" class="mr-1"/> Tarja:</label>
              <v-select
                v-model="form.tarja"
                :items="tarjaOptions"
                placeholder="Selecione"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
                menu-icon="mdi-chevron-down"
              ></v-select>
            </div>
          </v-col>

          <v-col cols="12" md="4" class="pl-md-8">
            <div class="mb-4">
              <label class="input-label"><v-icon icon="mdi-package-variant" size="small" class="mr-1"/> Caixas:</label>
              <div class="custom-stepper">
                <v-btn icon size="x-small" variant="text" @click="updateNumber('caixas', -1)">
                  <v-icon>mdi-chevron-left</v-icon>
                </v-btn>
                <input type="number" v-model="form.caixas" readonly class="stepper-input">
                <v-btn icon size="x-small" variant="text" @click="updateNumber('caixas', 1)">
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </div>
            </div>

            <div class="mb-4">
              <label class="input-label"><v-icon icon="mdi-grid" size="small" class="mr-1"/> Quantidade:</label>
              <div class="d-flex align-center">
                <div class="custom-stepper mr-2">
                  <v-btn icon size="x-small" variant="text" @click="updateNumber('qtdPorCaixa', -1)">
                    <v-icon>mdi-chevron-left</v-icon>
                  </v-btn>
                  <input type="number" v-model="form.qtdPorCaixa" readonly class="stepper-input">
                  <v-btn icon size="x-small" variant="text" @click="updateNumber('qtdPorCaixa', 1)">
                    <v-icon>mdi-chevron-right</v-icon>
                  </v-btn>
                </div>
                <span class="text-caption text-slate-600">Unidades por Caixa</span>
              </div>
            </div>

            <div>
              <label class="input-label"><v-icon icon="mdi-eyedropper" size="small" class="mr-1"/> Dosagem:</label>
              <div class="d-flex ga-2">
                <v-text-field
                  v-model="form.dosagem"
                  placeholder="00"
                  variant="solo"
                  bg-color="#f1f5f9"
                  flat
                  hide-details
                  class="rounded-input flex-grow-1"
                ></v-text-field>
                <v-select
                  v-model="form.dosagemUnidade"
                  :items="unidadeOptions"
                  variant="solo"
                  bg-color="#f1f5f9"
                  flat
                  hide-details
                  class="rounded-input"
                  style="max-width: 100px;"
                  menu-icon="mdi-chevron-down"
                ></v-select>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-card>

      <v-card class="mb-6 pa-6" elevation="3" rounded="xl">
        <h2 class="section-title mb-6">Informações do Fabricante:</h2>

        <v-row dense>
          <v-col cols="12" md="7">
            <div class="mb-4">
              <label class="input-label"># Lote:</label>
              <v-text-field
                v-model="form.lote"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
              ></v-text-field>
            </div>

            <div class="mb-4">
              <label class="input-label"><v-icon icon="mdi-domain" size="small" class="mr-1"/> Fabricante:</label>
              <v-text-field
                v-model="form.fabricante"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
              ></v-text-field>
            </div>

            <div>
              <label class="input-label"><v-icon icon="mdi-file-document-outline" size="small" class="mr-1"/> Registro MS:</label>
              <v-text-field
                v-model="form.registroMs"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
              ></v-text-field>
            </div>
          </v-col>

          <v-col cols="12" md="5" class="pl-md-8">
            <div>
              <label class="input-label"><v-icon icon="mdi-calendar" size="small" class="mr-1"/> Validade:</label>
              <v-text-field
                v-model="form.validade"
                type="date"
                variant="solo"
                bg-color="#f1f5f9"
                flat
                hide-details
                class="rounded-input"
              ></v-text-field>
            </div>
          </v-col>
        </v-row>
      </v-card>

      <div class="d-flex justify-end">
        <v-btn
          color="slate600"
          size="large"
          class="concluir-btn px-10"
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

/* Tipografia e Cores */
.text-slate-900 { color: #0f172a; }
.text-slate-600 { color: #475569; }

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
}

/* User Button */
.user-btn {
  color: #475569 !important;
  text-transform: none;
  letter-spacing: normal;
}

/* Labels customizados */
.input-label {
  display: block;
  font-weight: 700;
  font-size: 0.9rem;
  color: #0f172a;
  margin-bottom: 8px;
}

/* Inputs arredondados estilo "Pill" ou com border-radius alto */
.rounded-input :deep(.v-field) {
  border-radius: 8px !important;
}

/* Custom Stepper (simulando o design < 1 >) */
.custom-stepper {
  display: inline-flex;
  align-items: center;
  background-color: #f1f5f9; /* slate-100 */
  border-radius: 8px;
  padding: 4px;
  height: 44px; /* Altura padrão do v-field comfortable */
}

.stepper-input {
  width: 40px;
  text-align: center;
  font-weight: 600;
  color: #475569;
  border: none;
  outline: none;
  background: transparent;
  -moz-appearance: textfield;
}

.stepper-input::-webkit-outer-spin-button,
.stepper-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Botão Concluir */
.concluir-btn {
  background-color: #334155 !important;
  color: white !important;
  font-weight: 600;
  text-transform: none;
}
</style>
