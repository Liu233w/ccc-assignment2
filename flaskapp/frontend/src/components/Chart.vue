<template>
  <v-chart class="chart" :option="option" />
</template>

<script>
import { THEME_KEY } from "vue-echarts";
export default {
  name: "Chart",
  provide: {
    [THEME_KEY]: "dark"
  },
  data() {
    return {
      option: {
        dataset: {
          dimensions: ['value', 'name'],
          source: [
            { value: 335, name: "Direct" },
            { value: 310, name: "Email" },
            { value: 234, name: "Ad Networks" },
            { value: 135, name: "Video Ads" },
            { value: 1548, name: "Search Engines" }
          ]
        },

        title: {
          text: "Traffic Sources",
          left: "center"
        },

        // tooltip: {},

        legend: {
          left: 'left',
          orient: "vertical"
        },

        tooltip: {
          trigger: 'item',
          formatter: (data) => {
            return data.name + ': ' + data.value.value
          }
        },
        // legend: {
        //   orient: "vertical",
        //   left: "left",
        //   data: [
        //     "Direct",
        //     "Email",
        //     "Ad Networks",
        //     "Video Ads",
        //     "Search Engines"
        //   ]
        // },
        series: [
          {
            name: "Traffic Sources",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            label: {
              formatter: '{@name}: {@value} ({d}%)'
            },
            encode: {
              value: 0,
              itemName: 1, //'name'
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      }
    }
  }
}
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>