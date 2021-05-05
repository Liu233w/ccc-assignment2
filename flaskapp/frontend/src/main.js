import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'

Vue.config.productionTip = false

import { CanvasRenderer } from "echarts/renderers";
import { PieChart, ScatterChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  DatasetComponent,
} from "echarts/components";

use([
  CanvasRenderer,
  ScatterChart,
  PieChart,
  DatasetComponent,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

// Register Echarts globally
Vue.component('v-chart', ECharts)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
