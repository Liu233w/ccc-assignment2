const state = {
    course: "",
    title: "",
    members: "",
    description: ""
}

const getters = {
    getSocket: (state, getters, rootState, rootGetters) => {
        return rootGetters['msgParserSocketStore/getSocket']
    },
    getCourse: (state) => {
        return state.course
    },
    getTitle: (state) => {
        return state.title
    },
    getMembers: (state) => {
        return state.members
    },
    getDescription: (state) => {
        return state.description
    },
};

const mutations = {
    setCourse(state, payload) {
        state.course = payload
    },
    setTitle(state, payload) {
        state.title = payload
    },
    setMembers(state, payload) {
        state.members = payload
    },
    setDescription(state, payload) {
        state.description = payload
    }
};

const actions = {
    subscribeSocket: ({ getters }) => {
        getters.getSocket.on('serviceEvent', (payload) => {
            if (payload.topic === "eventEmitExample") {
                // this matches with self.emit_event(topic="eventEmitExample", payload=payload) from backend
                console.log(`topic = "eventEmitExample", received payload = ${payload.payload}`)
            }
        })
    },
    getProjectInfo: ({ getters, commit }) => {
        getters.getSocket.emit('getProjectInfo', (resp) => {
            const respObj = JSON.parse(resp)
            commit("setCourse", respObj.course)
            commit("setTitle", respObj.title)
            commit("setMembers", respObj.members)
            commit("setDescription", respObj.description)
        })
    },
    testBackendEventEmitExample: ({ getters }) => {
        const payload = "Communication message."
        // if no result is returned via response, then there is no need to wait for response
        getters.getSocket.emit('eventEmitExample', payload)
    }
};

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}
