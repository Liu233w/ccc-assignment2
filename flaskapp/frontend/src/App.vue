<template>
  <keep-alive>
    <router-view />
  </keep-alive>
</template>

<script>

import {mapActions} from "vuex";

export default {
  name: "App",

  components: {},

  data: () => ({}),

  methods: {
    ...mapActions("msgParserSocketStore", ["connectSockets"]),
  },
  created() {
    console.log("app page is created");
    this.connectSockets();
  },

  activated() {
  },
};
</script>

<style lang="scss">
</style>
