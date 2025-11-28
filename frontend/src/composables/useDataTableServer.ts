import {onMounted, ref, watch} from 'vue';
      import axios from 'axios';

      const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

      export function useDataTableServer(apiUrl: string, initialOptions?: any) {
        const useParams = ref<boolean>(
          initialOptions !== undefined && Object.keys(initialOptions || {}).length > 0
        );

        const options = ref<any>(
          useParams.value
            ? {
              page: 1,
              itemsPerPage: 10,
              sortBy: [],
              search: undefined,
              ...initialOptions,
            }
            : {}
        );

        const items = ref<any[]>([]);
        const totalItems = ref(0);
        const loading = ref(false);

        const fetchItems = async () => {
          loading.value = true;
          try {
            let params: any = undefined;

            if (useParams.value) {
              params = {
                page: options.value.page,
                itemsPerPage: options.value.itemsPerPage,
                sortBy: JSON.stringify(options.value.sortBy || []),
                search: options.value.search || '',
              };
            }

            const response = await axios.get(API_BASE_URL + apiUrl, params ? {params} : undefined);

            const data = response.data;

            if (Array.isArray(data)) {
              items.value = data;
              totalItems.value = data.length;
            } else if (Array.isArray(data.records)) {
              items.value = data.records;
              totalItems.value = data.total ?? data.records.length ?? 0;
            } else if (Array.isArray(data.data)) {
              items.value = data.data;
              totalItems.value = data.total ?? data.data.length ?? 0;
            } else {
              items.value = [];
              totalItems.value = 0;
            }
          } catch (error) {
            console.error('Error fetching data:', error);
            items.value = [];
            totalItems.value = 0;
          } finally {
            loading.value = false;
          }
        };

        watch([options, useParams], fetchItems, {deep: true});

        onMounted(fetchItems);

        const updateOptions = (newOptions: any) => {
          if (!useParams.value) {
            options.value = {
              page: 1,
              itemsPerPage: 10,
              sortBy: [],
              search: undefined,
              ...newOptions,
            };
            useParams.value = true;
          } else {
            Object.assign(options.value, newOptions);
          }
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
