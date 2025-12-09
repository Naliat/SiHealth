<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Chart, registerables } from 'chart.js'; 

Chart.register(...registerables); 

interface Dataset {
    data: number[];
    label: string;
}

const props = defineProps<{
    data: Dataset[]; 
    labels: string[];
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let lineChart: Chart | null = null;

const createChart = () => {
  if (!chartCanvas.value || !props.data.length || !props.data[0].data.length) {
    if (lineChart) {
      lineChart.destroy();
      lineChart = null;
    }
    return;
  }

  const chartData = {
    labels: props.labels,
    datasets: props.data.map(dataset => ({
      ...dataset,
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      tension: 0.4, 
      fill: true, 
      pointRadius: 4, 
    }))
  };

  if (lineChart) {
    lineChart.data.labels = chartData.labels as string[];
    lineChart.data.datasets = chartData.datasets;
    lineChart.update();
  } else {
    lineChart = new Chart(chartCanvas.value, {
      type: 'line',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          x: { grid: { display: false } },
          y: { 
            beginAtZero: true,
            ticks: { maxTicksLimit: 5 },
          }
        }
      }
    });
  }
};

onMounted(() => {
  createChart();
});

watch([() => props.data, () => props.labels], () => {
  createChart();
}, { deep: true });
</script>

<style scoped>
.chart-container {
    height: 100%; 
}
</style>