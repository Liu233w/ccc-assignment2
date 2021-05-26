const state = {
  list: null,
  autoRefreshing: false,
}

const mutations = {
  saveList(state, value) {
    state.list = value
  },

  setAutoRefreshing(state, bool) {
    state.autoRefreshing = bool
  }
}

const actions = {
  async refresh({commit}) {
    const res = await this._vm.$axios.get('/api/analysis/suburb_category/record')
    commit('saveList', res.data.result)
  },

  startAutoRefreshing({commit, dispatch, state}) {
    if (state.autoRefreshing) {
      return
    }

    commit('setAutoRefreshing', true)

    const timer = async () => {
      await dispatch('refresh')
      setTimeout(timer, 5000)
    }

    timer()
  }
}

const getters = {
  suburb(state) {
    if (!state.list) {
      return {}
    }

    const res = {}
    state.list.forEach(item => {
      const suburb = item.key[0]
      const category = item.key[1]

      if (!res[suburb]) {
        res[suburb] = {}
      }

      res[suburb][category] = item.value
    })

    return res
  }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}

