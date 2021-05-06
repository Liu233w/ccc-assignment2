<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <Chart></Chart>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Chart from '../components/Chart.vue'

export default {
  name: "ChartView",
  components: {
    Chart,
  }
}
</script>

<style scoped>

</style>