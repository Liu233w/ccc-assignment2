const state = {
    token: 'AIzaSyBObuayOsssm6Zkmi46aRDizkbdr1wJSGo',
    options: {
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: true,
        disableDefaultUi: false,
        zoom: 10,
        center: {lat: -37.840935, lng: 144.946457},
        style: "width: 500px; height: 300px"
    }
}

const mutations = {
    setToken(state, payload) {
        state.token = payload
    }
}

const actions = {

}

const getters = {
    getToken(state){
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

