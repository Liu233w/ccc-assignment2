const state = {
    token: 'AIzaSyBObuayOsssm6Zkmi46aRDizkbdr1wJSGo'
}

const mutations = {
    setToken(state, payload) {
        state.token = payload
    }
}

const actions = {

}

const getters = {
    getToken(){
        return state.token
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}

