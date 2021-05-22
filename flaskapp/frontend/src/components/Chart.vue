<template>
  <p v-if="!loaded">No data</p>
  <v-chart v-else class="chart" :option="option"/>
</template>

<script>
import {THEME_KEY} from "vue-echarts";

export default {
  name: "Chart",
  provide: {
    [THEME_KEY]: "shine" // dark, vintage, macarons, infographic, roma
  },

  props: ['rename'],

  data() {
    return {
      loaded: false,

      option: {
        dataset: {
          dimensions: ['value', 'name'],
          source: [
            {value: 335, name: "Pets"},
            {value: 310, name: "IT"},
            {value: 234, name: "Cars"},
            {value: 135, name: "Sports"},
            {value: 1548, name: "Food"},
            {value: 500, name: "Others"}
          ]
        },

        title: {
          text: 'suburb',
          left: 'center'
        },

        // tooltip: {},

        legend: {
          bottom: 'bottom',
          orient: "horizontal"
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
            center: ["50%", "50%"],
            label: {
              formatter: '{@name}: {d}%'
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
  },

  watch: {
    rename(value) {
      this.loaded = false

      this.option.title.text = value
      
      const suburb = this.$store.getters['categories/suburb'][value.toUpperCase()]
      if (!suburb || suburb.length <= 0) {
        return
      }

      const res = []
      for (const category in suburb) {
        if (category === 'OTHER') {
          continue
        }
        const value = suburb[category]
        res.push({value, name: category})
      }
      this.$set(this.option.dataset, 'source', res)
      this.loaded = true
    }
  }
}
</script>

<style scoped>
.chart {
  height: 400px;
  width: 600px;
}
</style>