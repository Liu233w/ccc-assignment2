import Vue from 'vue'
import Vuex from 'vuex'
import msgParserSocketStore from './msgParserSocketStore'
import homePanelStore from './homePanelStore'

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
    homePanelStore
  }
})
