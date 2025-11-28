<template>
  <v-app>
    <SideBar/>
    <v-main>
      <v-container class="pa-0" fluid>
        <router-view/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import SideBar from '@/components/layout/SideBar.vue'
</script>

<style scoped>
</style>
