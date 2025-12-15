<template>
  <canvas 
        ref="chartCanvas" 
        :style="{ height: `${dynamicChartHeight}px` }"
      />
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { Chart, registerables } from 'chart.js'; 

Chart.register(...registerables); 

interface DataPoint {
    label: string;
    value: number;
}

const props = defineProps<{
    data: DataPoint[]; 
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let barChart: Chart | null = null;

const BAR_HEIGHT_PX = 30; 
const MIN_CHART_HEIGHT_PX = 150; 

const dynamicChartHeight = computed(() => {
    const calculatedHeight = (props.data.length * BAR_HEIGHT_PX) + 50; 
     
    return Math.max(calculatedHeight, MIN_CHART_HEIGHT_PX);
});


const createChart = () => {
  if (!chartCanvas.value || !props.data.length) {
    if (barChart) {
      barChart.destroy();
      barChart = null;
    }
    return;
  }
  
  const chartData = {
    labels: props.data.map(p => p.label),
    datasets: [{
      data: props.data.map(p => p.value),
      label: 'Quantidade Retirada',
      backgroundColor: '#15803d', 
      borderColor: '#15803d',
      borderWidth: 1,
    }]
  };

  if (barChart) {
    barChart.data.labels = chartData.labels as string[];
    barChart.data.datasets = chartData.datasets;
    barChart.update();
  } else {
    barChart = new Chart(chartCanvas.value, {
      type: 'bar',
      data: chartData,
      options: {
        indexAxis: 'y',
        resize: false, 
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          x: { 
            beginAtZero: true,
            grid: { display: false },
            ticks: { precision: 0 }
          },
          y: { 
            grid: { display: true, color: '#e5e7eb' }
          }
        }
      }
    });
  }
};

onMounted(() => {
  createChart();
});

watch(() => props.data, () => {
  createChart();
}, { deep: true });
</script>

<style scoped>
</style>