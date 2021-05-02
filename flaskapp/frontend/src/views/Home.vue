<template>
  <div class="home">
      <v-container fluid class="px-2">
        <v-row dense>
            <h1>{{getCourse}}</h1>
            <h2>{{getTitle}}</h2>
            <p>{{getMembers}}</p>
            <p>{{getDescription}}</p>
        </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters} from 'vuex'

export default {
  name: 'Home',

  components: {
  },

  data: () => ({
  }),

  computed: {
    ...mapGetters('homePanelStore', ['getCourse', 'getTitle', 'getMembers', 'getDescription']),
  },

  methods: {
    ...mapActions('homePanelStore', ['getProjectInfo', 'subscribeSocket', 'testBackendEventEmitExample']),
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
