<script lang="ts" setup>
  import { ref, watch } from 'vue'
  import { useDataTableServer } from '@/composables/useDataTableServer'

  const search = ref('')
  const displaySort = ref('Alfabética')

  const { items, loading, totalItems, options } = useDataTableServer('/medicamentos')

  options.value = {
    ...options.value,
    itemsPerPage: 10,
    sortBy: [{ key: 'nome', order: 'asc' }],
  }

  let searchTimeout: ReturnType<typeof setTimeout>

  watch(search, newVal => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      options.value = { ...options.value, search: newVal }
    }, 500)
  })

  function getStatusClass (status: string) {
    switch (status) {
      case 'OK': {
        return 'status-ok'
      }
      case 'Próx. Venc.': {
        return 'status-warning'
      }
      case 'Vencido': {
        return 'status-expired'
      }
      default: {
        return ''
      }
    }
  }
</script>

<template>
  <v-container class="page-container pa-8 bg-gradient" fluid>

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
        class="custom-table"
        hide-default-footer
        :items="items"
        :items-length="totalItems"
        :loading="loading"
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
            <th class="text-left pa-4" style="width: 50%; max-width: 50%;">
              <div class="d-flex align-center ga-2">
                <span class="header-icon">Tt</span>
                <span class="header-text">Nome do remédio</span>
              </div>
            </th>
            <th class="pa-4" style="width: 2%; max-width: 2%" />
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
                {{ item.id_medicamento }}
              </div>
            </td>

            <td class="text-left pa-5">
              <div class="d-flex align-center">
                <div class="vertical-divider" />
                <span class="medicine-name">{{ item.nome ?? '-' }}</span>
              </div>
            </td>

            <td class="pa-5" />

            <td class="text-center pa-5">
              <v-chip
                class="status-chip"
                :class="getStatusClass(item.status ?? '')"
                size="small"
              >
                {{ item.status ?? '—' }}
              </v-chip>
            </td>

            <td class="text-center pa-5">
              <v-tooltip location="top" text="Ver detalhes do remédio">
                <template #activator="{ props }">
                  <v-btn
                    class="action-btn"
                    icon
                    size="small"
                    v-bind="props"
                  >
                    <v-icon size="20">mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
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
                >
                  Gerar relatório da lista de remédios
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
</style>
