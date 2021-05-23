<template>
  <div class="graph">
    <v-parallax dark src="../assets/city.png">
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="display-1 font-weight-bold mb-4">Findings</h1>
          <h2>
            As we targeted on analysing the relationship between the topics
            people are interested and their geometric locations in Great Melbourne
            Area, we selected five main regions to demonstrate our findings. <br />
          </h2>
        </v-col>
      </v-row>
    </v-parallax>
    <v-row justify="center">
      <v-col cols="12" align-self="center">
        <v-card class="mb-30">
          <v-tabs
            v-model="tab"
            background-color="teal darken-3"
            centered
            dark
          >

            <v-tab v-for="item in items" :key="item.region">
              {{ item.region }}
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab">
            <v-tab-item v-for="item in items" :key="item.region">
              <v-row>
                <v-col cols="6" align-self="center" class="mx-10">
                  <p class="my-20"></p>
                  <v-img :src="require(`@/assets/${item.image}.png`)" max-height="470" contain />
                  <p class="mt-30">Note: This graph is generated based on tweets harvested until 23rd May 2021.</p>
                </v-col>
                <v-col cols="4" align-self="center">
                  <h3>{{item.text}}</h3>
                </v-col>
              </v-row>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "Graph",
  data() {
    return {
      tab: null,
      items: [
        {
          region: "ALTONA",
          image: "Altona",
          text:
            "As according to the graph, people in Altona tweet mostly about sport, food and music compared to other suburbs. Altona Beach Festival and musicals performed at Altona Civic Theatre provide people with opportunities to enjoy food and music. Altona is also home to many sporting clubs including Australian rules football, soccer, cricket, etc.",
        },
        {
          region: "CLAYTON",
          image: "Clayton",
          text:
            "Compared to other suburbs, a higher percentage of people tweet about politics, gaming and technology. The reason could be that there might be more young adults and student living and travelling in this region as Monash University is based in Clayton.",
        },
        {
          region: "GLEN WAVERLEY",
          image: "GlenWaverley",
          text:
            "Tweets collected in Glen Waverley show that people in this region are more interested in entertainment, food and sport. Glen Waverley houses many eateries, retail stores and entertainment facilities. It also has a large shopping center, many sports facilities like golf course and sports clubs like tennis and basketball clubs.",
        },
        {
          region: "MELBOURNE",
          image: "Melbourne",
          text:
            "There is a great diversity in the topics that people tweet about, which is as expected as there is a diverse range of businesses and people working, living and travelling in this region.",
        },
        {
          region: "NORTH MELBOURNE",
          image: "NorthMelbourne",
          text:
            "Above 75% of the people tweet about sports in this region. The reason might be that North Melbourne Football Club is based in this region, which plays in the national Australian football competition.",
        },
      ],
    };
  },
};
</script>

<style scoped lang="scss">
</style>