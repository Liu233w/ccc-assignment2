import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import * as GmapVue from 'gmap-vue'
import axios from 'axios'

Vue.config.productionTip = false

import { CanvasRenderer } from "echarts/renderers";
import { PieChart, ScatterChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  DatasetComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent,
  TimelineComponent,
  CalendarComponent
} from "echarts/components";

use([
  CanvasRenderer,
  ScatterChart,
  PieChart,
  DatasetComponent,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent,
  TimelineComponent,
  CalendarComponent
]);

// Register Echarts globally
Vue.component('v-chart', ECharts)

Vue.use(GmapVue, {
  load: {
    key: 'AIzaSyD80YokVTEspwIFbtwyTSEn7V0xm1ypzGo',
  },
  installComponents: true
})

// add axios
const axiosInstance = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? 'http://localhost:9797' : '/'
})
Vue.prototype.$axios = axiosInstance

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
