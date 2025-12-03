<script lang="ts" setup>
import {ref} from 'vue'

interface SideBarItem {
  title: string
  icon: string
  value: string
  route: {
    path: string
  }
}

const selectedItem = ref<string>('dashboard')

const menuItems: SideBarItem[] = [
  {title: 'Dashboard', icon: 'mdi-view-dashboard', value: 'dashboard', route: {path: 'dashboard'}},
  {title: 'Lista do Estoque', icon: 'mdi-format-list-bulleted', value: 'estoque', route: {path: 'estoque'}},
  {title: 'Lista de Medicamentos', icon: 'mdi-clipboard-list', value: 'medicamentos', route: {path: 'medicamentos'}},
  {title: 'Registrar Lote', icon: 'mdi-plus-box-multiple-outline', value: 'novo-lote', route: {path: 'registrarLote'}},
  {title: 'Registrar Saída', icon: 'mdi-exit-to-app', value: 'saida', route: {path: 'registrar-saida'}},
   {title: 'Registrar Remédio', icon: 'mdi-pill', value: 'novo-remedio', route: { path: 'registrarRemedio' }},
]

const bottomItems: SideBarItem[] = [
  {title: 'Configurações', icon: 'mdi-cog', value: 'config', route: {path: 'configuracao'}}, 
  {title: 'Sair', icon: 'mdi-logout', value: 'sair', route: {path: 'login'}}, 
]
</script>

<template>
  <v-navigation-drawer color="#3b5b76" permanent width="280">
    <div class="pa-16 d-flex align-center">
      <v-icon class="mr-3" icon="mdi-hospital-box" size="large"/>
      <span class="text-h6 font-weight-bold">SiHealth</span>
    </div>

    <v-list v-model="selectedItem" class="pa-0" density="compact" nav>
      <v-list-item
        v-for="(item, i) in menuItems"
        :key="i"
        :prepend-icon="item.icon"
        :title="item.title"
        :to="item.route"
        :value="item.value"
        active-class="custom-active-item"
        class="mb-2 pl-6"
      />
    </v-list>
    <template #append>
      <v-list v-model="selectedItem" class="pa-0 mb-4" density="compact" nav>
        <v-list-item
          v-for="(item, i) in bottomItems"
          :key="i"
          :prepend-icon="item.icon"
          :title="item.title"
          :to="item.route"
          :value="item.value"
          class="pl-6"
        />
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<style scoped>

:deep(.v-list-item-title) {
  font-size: 0.95rem;
  font-weight: 500;
}
</style>