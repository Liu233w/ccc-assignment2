<template>
  <v-row>
    <v-col cols="12">
      <Chart></Chart>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "ChartVIew",
  component: {
    Chart: () => import('../components/Chart.vue')
  }
}
</script>

<style scoped>

</style>