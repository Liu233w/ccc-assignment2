<template>
  <div class="home">
      <v-container fluid class="px-2">
        <v-row dense>
            <h1>{{getCourse}}</h1>
            <h2>{{getTitle}}</h2>
            <p>{{getMembers}}</p>
            <p>{{getDescription}}</p>
            <v-btn
              color="red lighten-2"
              dark
            >
              Click Me
            </v-btn>
            <!-- <v-col cols="2" class="pa-0" align-self="center">
              <v-btn @click="postRequestToBackend()">
                Post To Backend
              </v-btn>
              <p>Post Request Response: {{ postRequestResponse }}</p>
            </v-col> -->
        </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters} from 'vuex'
const axios = require('axios').default;

export default {
  name: 'Home',

  components: {
  },

  data: () => ({
    postRequestResponse: ""
  }),

  computed: {
    ...mapGetters('msgParserSocketStore', ['getUrlAddress']),
    ...mapGetters('homePanelStore', ['getCourse', 'getTitle', 'getMembers', 'getDescription']),
  },

  methods: {
    ...mapActions('homePanelStore', ['getProjectInfo', 'subscribeSocket', 'testBackendEventEmitExample']),
    postRequestToBackend() {
            const urlAddress = `${this.getUrlAddress}:9797}:/api/services/post-example`
            const payload = {"request": "post request from frontend"}
            return axios.post(urlAddress,
                payload
        ).then(function (resp) {
            // returned response from back-end is in format {"response": "post request is successful"}
            this.postRequestResponse = resp.reponse
          }
        ).catch(function () {
            console.log('Failed to handle post request!')
        });
    }
  },

  created(){
    this.subscribeSocket()
    this.getProjectInfo()
  },

  activated(){
    this.testBackendEventEmitExample()
  }
}
</script>
