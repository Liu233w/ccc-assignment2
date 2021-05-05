<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
      <h1>Connected: {{ getConnectionStatus }}</h1>
    </div>
    <keep-alive>
      <router-view class="pa-0" />
    </keep-alive>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "App",

  components: {},

  data: () => ({}),

  computed: {
    ...mapGetters("msgParserSocketStore", ["getConnectionStatus"]),
  },

  methods: {
    ...mapActions("msgParserSocketStore", ["connectSockets"]),
  },

  created() {
    console.log("app page is created");
    this.connectSockets();
  },

  activated() {},
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
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
