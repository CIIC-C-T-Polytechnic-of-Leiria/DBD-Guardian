<template>
  <div class="graph-container">
  <button class="close-button" @click="closeGraph">×</button>
  <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script>
import ApexCharts from 'apexcharts';
import { ref, onMounted, watch } from 'vue';

export default {
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  methods: {
    closeGraph() {
      this.$emit('closeGraph', this.data.query);
    },
  },
  setup(props) {
    const chart = ref(null);
    const chartContainer = ref(null);

    watch(
  () => props.data,
  (newVal) => {

    // Check for "No results found" in any part of the result string
    if (newVal.result.some((item) => item.includes("No results found"))) {
      if (chart.value) {
        chart.value.updateOptions({
          xaxis: {
            categories: ["No results found"],
          },
          series: [
            {
              name: "No results found",
              data: [null],
            },
          ],
        });
      }
      return;
    }

    const categories = newVal.result.map((item) =>
      item[0].split('#')[2].trim()
    );
    const seriesName = newVal.result[0][0]
      .split('#')[3]
      .trim()
      .slice(0, -1); // remove trailing ':'
    const seriesData = newVal.result.map((item) =>
      parseInt(item[0].split('#')[4].trim().split(' ')[0])
    );

    if (chart.value) {
      chart.value.updateOptions({
        xaxis: {
          categories,
        },
        series: [
          {
            name: seriesName,
            data: seriesData,
          },
        ],
      });
    }
  },
  { deep: true }
);

    onMounted(() => {
      const options = {
        series: [
          {
            name: props.data.query,
            data: [],
          },
        ],
        chart: {
          type: props.data.graphType,
          height: 350,
         
        },
        title: {
            text: props.data.query, // Adjusted placement of 'title' key
            align: 'center',
          },
        xaxis: {
          categories: [],
        },
      };

      chart.value = new ApexCharts(chartContainer.value, options);
      chart.value.render();
    });

    return { chartContainer };
  },
};
</script>


<style scoped>
.graph-container {
  position: relative;
  /* Other styles for the graph container */
}


.close-button {
  background-color: bisque;
  border: none;
  position: absolute;
  font-size: 20px;
  top: -30px;
  right: 10px;
  cursor: pointer;
}

.close-button:hover {
  background-color: #f44336;
  color: white;
}
</style>
