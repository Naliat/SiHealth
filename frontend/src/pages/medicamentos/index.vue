<template>
  <div>
    <h1 v-if="loading">Loading...</h1>
    <table v-else>
      <thead>
      <tr>
        <th>Name</th>
        <th>Position</th>
        <th>Office</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in items" :key="item.id">
        <td>{{ item.name }}</td>
        <td>{{ item.position }}</td>
        <td>{{ item.office }}</td>
      </tr>
      </tbody>
    </table>

    <div>
      <button @click="updateOptions({ page: options.page - 1 })" :disabled="options.page === 1">Previous</button>
      <span>Page {{ options.page }} of {{ Math.ceil(totalItems / options.itemsPerPage) }}</span>
      <button @click="updateOptions({ page: options.page + 1 })">Next</button>
    </div>
  </div>
</template>

<script setup lang="ts">

import {useDataTableServer} from "@/composables/useDataTableServer.ts";

const { items, loading, totalItems, options, updateOptions } = useDataTableServer('/api/');

</script>
