import Socket from 'socket.io-client'

// initial state
const state = {
    urlAddress: `http://${location.hostname}:9797`,
    msgParserSocket: Socket(`${location.hostname}:9797/msg-parser`),
    socketConnectedFlag: false
}

// getters
const getters = {
    getUrlAddress: (state) => {
        return state.urlAddress
    },
    getSocket: (state) => {
        return state.msgParserSocket
    },
    getConnectionStatus: (state) => {
        return state.socketConnectedFlag
    }
}

// mutations MUST be synchronous
const mutations = {
    setSocketConnectedFlag(state, payload) {
        state.socketConnectedFlag = payload
    }
}

// actions can by async, you can perform async operations here
const actions = {
    connectSockets: ({ state, commit }) => {
        // self.on('connect', payload) in msg_parser_socketio_server.py will listen to this payload
        state.msgParserSocket.on('connect', () => {
            console.log("connected")
            commit('setSocketConnectedFlag', true)
        })
        state.msgParserSocket.on('disconnect', () => {
            commit('setSocketConnectedFlag', false)
        })
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}
