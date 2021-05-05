<template>
  <div class="home">
      <v-container fluid class="px-2">
        <v-row dense>
          <v-col cols="12">
            <h1>{{getCourse}}</h1>
            <h2>{{getTitle}}</h2>
            <p>{{getMembers}}</p>
            <p>{{getDescription}}</p>
            <v-btn @click="postRequestToBackendHandler()">
              Post To Backend
            </v-btn>
            <p>Post Request Response: {{ postRequestResponse }}</p>
          </v-col>
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
            this.postRequestResponse = ""
            // urlAddress: 'http://localhost:9797/api/services/post-example'
            const urlAddress = `${this.getUrlAddress}/api/services/post-example`
            const payload = {"request": "post request from frontend"}
            return axios.post(urlAddress, payload).then(function (resp) {
                // resp: data,[object Object],status,200,statusText,OK,headers,[object Object],config,[object Object],request,[object XMLHttpRequest]
                // data returned from backend is contained in: resp.data
                // resp.data = {"response": "post request is successful"} <- response from backend
                let result = resp.data.response
                console.log(`post request result received: ${result}`)
                return result
              }
            ).catch(err => {
                console.log(`${err}`)
                return err
            });
    },
    postRequestToBackendHandler() {
        const returnResult = this.postRequestToBackend()
        returnResult.then((resp) => {
            this.postRequestResponse = resp
        })
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
