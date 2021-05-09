<template>
  <v-chart class="chart" :option="option"/>
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

      option: {
        dataset: {
          dimensions: ['value', 'name'],
          source: [
            {value: 335, name: "Pets"},
            {value: 310, name: "IT"},
            {value: 234, name: "Cars"},
            {value: 135, name: "Sports"},
            {value: 1548, name: "Food"}
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
              show: false,
              position: 'center'
            },
            // label: {
            //   formatter: '{@name}: {@value} ({d}%)'
            // },
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

  methods: {

    // setChartTitle() {
    //   const new_option = this.option
    //   this.option.title.text = this.rename
    //   this.option = new_option
    // }

  }
}
</script>

<style scoped>
.chart {
  height: 400px;
  width: 600px;
}
</style>