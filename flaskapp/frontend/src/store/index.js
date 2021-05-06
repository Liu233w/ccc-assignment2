import Vue from 'vue'
import Vuex from 'vuex'
import msgParserSocketStore from './msgParserSocketStore'
import homePanelStore from './homePanelStore'
import googleMap from "./googleMap"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    msgParserSocketStore,
    homePanelStore,
    googleMap,
  }
})
