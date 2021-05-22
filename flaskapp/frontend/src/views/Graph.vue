<template>
  <div class="graph">
    <v-parallax dark src="../assets/city.png">
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="display-1 font-weight-bold mb-4">
            Stastical Analysis
          </h1>
          <h2>As we targeted on analysing the relationship between the products people are interested
            and people's occupation in Greate Melbourne Area, we selected five main regions to demonstrate
            our findings, which can be referred to in the histogram below. <br/>
            Describe our major findings here: .......
          </h2>
        </v-col>
      </v-row>
    </v-parallax>
    <v-row justify="center">
      <v-col cols="12" align-self="center">
        <v-chart></v-chart>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Chart from "../components/Chart"

export default {
  name: "Graph",
  components: {
    'v-chart': Chart
  },
};
</script>

<style scoped lang="scss">
</style>