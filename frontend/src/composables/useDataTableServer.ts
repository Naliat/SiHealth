import {onMounted, ref, watch} from 'vue';

export function useDataTableServer(apiUrl: string, initialOptions = {}) {
  const items = ref([]);
  const totalItems = ref(0);
  const loading = ref(false);
  const options = ref({
    page: 1,
    itemsPerPage: 10,
    sortBy: [],
    search: undefined,
    ...initialOptions,
  });

  const fetchItems = async () => {
    loading.value = true;
    try {
      const queryParams = new URLSearchParams({
        page: options.value.page.toString(),
        itemsPerPage: options.value.itemsPerPage.toString(),
        sortBy: JSON.stringify(options.value.sortBy),
        search: options.value.search || '',
      });

      const response = await fetch(`${apiUrl}?${queryParams.toString()}`);
      if (!response.ok) {
        items.value = [];
        totalItems.value = 0;
        return;
      }

      const data = await response.json();
      items.value = data.records;
      totalItems.value = data.total;
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      loading.value = false;
    }
  };

  watch(options, fetchItems, {deep: true});

  onMounted(fetchItems);

  const updateOptions = (newOptions: any) => {
    Object.assign(options.value, newOptions);
  };

  return {
    items,
    totalItems,
    loading,
    options,
    updateOptions,
    fetchItems,
  };
}
