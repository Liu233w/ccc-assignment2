<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dense
      dark
    >
      <v-toolbar-title>
        Team 2 Project App
      </v-toolbar-title>
      <div class="justify-end">
        <v-btn color="success" class="ma-2 white--text" @click="$router.push('/')">Home</v-btn>
        <v-btn color="success" class="ma-2 white--text" @click="$router.push('/demo')">Map</v-btn>
      </div>
    </v-app-bar>

    <v-main>
      <keep-alive>
        <router-view class="pa-0"/>
      </keep-alive>

    </v-main>
  </v-app>
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
