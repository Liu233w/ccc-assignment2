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
          This application aims to show what types of products people are
          interested in different regions in Greate Melbourne Area and how this
          is related to people's occupations. The analysis regarding people's
          interests in different products is conducted based on twitter data
          harvested. Product range includes Sport, IT, Cooking and Food,
          Education, Pet, etc. Occupation by age in different regions is
          retrieved from AURIN, which gets mapped to people's interests to
          demonstrate the trend.<br />
          Analysis panel allows user to interact with the data via selecting regions
          in goolge map and results will be displayed accordingly.<br />
          Findings panel displays a sample result in the format of histogram to demonstrate
          how people's interests in different products is related to their occupation in 
          different regions.
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