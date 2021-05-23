<template>
  <div class="home">
    <v-parallax dark src="../assets/background.png">
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="display-1 font-weight-bold mb-4">
            [COMP90024] Cluster and Cloud Computing
          </h1>
          <h1 class="subheading">Assignment 2 Project App</h1>
          <h2 class="subheading">Team 2 Members</h2>
          <h4 class="subheading">
            Shumin Liu, Ying Mao, Jiexin Liu, Keshawa Jay, Rob Sloan
          </h4>
        </v-col>
      </v-row>
    </v-parallax>
    <v-row justify="center">
      <v-col cols="6" align-self="center">
        <h1 class="text-center">Project Description</h1>
        <v-divider></v-divider>
        <p class="mt-10">
          This application analyzed what kind of topics people are interested in different regions of Great Melbourne Area.
          Twitter data are harvested and categorized into 10 categories, which are entertainment, business, technology, gaming, music, sports, 
          politics, fashion, health and food.<br /><br />
          Analysis panel allows user to interact with the live data via selecting the region
          in goolge map to obtain the result of that region. Result is displayed in the format of pie charts, which shows 
          the number of tweets that is relevant to a particular topic in percentage.<br /><br />
          Findings panel displays the results collected from five suburbs to demonstrate our findings in more details.
        </p>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

const axios = require("axios").default;

export default {
  name: "Home",

  components: {},

  data: () => ({
    postRequestResponse: "",
    getRequestResponse: "",
  }),

  computed: {
    ...mapGetters("msgParserSocketStore", [
      "getUrlAddress",
      "getConnectionStatus",
    ]),
    ...mapGetters("homePanelStore", [
      "getCourse",
      "getTitle",
      "getMembers",
      "getDescription",
    ]),
  },

  methods: {
    ...mapActions("homePanelStore", [
      "getProjectInfo",
      "subscribeSocket",
      "testBackendEventEmitExample",
    ]),

    postRequestToBackend() {
      this.postRequestResponse = "";
      // urlAddress: 'http://localhost:9797/api/services/post-example'
      const urlAddress = `${this.getUrlAddress}/api/services/post-example`;
      const payload = { request: "post request from frontend" };
      return axios
        .post(urlAddress, payload)
        .then(function (resp) {
          // resp: data,[object Object],status,200,statusText,OK,headers,[object Object],config,[object Object],request,[object XMLHttpRequest]
          // data returned from backend is contained in: resp.data
          // resp.data = {"response": "post request is successful"} <- response from backend
          let result = resp.data.response;
          console.log(`POST request result received: ${result}`);
          return result;
        })
        .catch((err) => {
          console.log(`${err}`);
          return err;
        });
    },
    postRequestToBackendHandler() {
      const returnResult = this.postRequestToBackend();
      returnResult.then((resp) => {
        this.postRequestResponse = resp;
      });
    },

    getRequestToBackend() {
      this.getRequestResponse = "";
      // urlAddress: 'http://localhost:9797/api/services/post-example?id=1234'
      const urlAddress = `${this.getUrlAddress}/api/services/get-example?id=1234`;
      // const payload = { id: 1234 };
      return axios
        .get(urlAddress)
        .then(function (resp) {
          // resp: data,[object Object],status,200,statusText,OK,headers,[object Object],config,[object Object],request,[object XMLHttpRequest]
          // data returned from backend is contained in: resp.data
          // resp.data = {"response": "post request is successful"} <- response from backend
          let result = resp.data.response;
          console.log(`GET request result received: ${result}`);
          return result;
        })
        .catch((err) => {
          console.log(`${err}`);
          return err;
        });
    },
    getRequestToBackendHandler() {
      const returnResult = this.getRequestToBackend();
      returnResult.then((resp) => {
        this.getRequestResponse = resp;
      });
    },
  },

  created() {
    this.subscribeSocket();
    this.getProjectInfo();
  },

  activated() {
    this.testBackendEventEmitExample();
  },
};
</script>

<style scoped lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-image: url("/images/background.png");
  background-size: cover;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>