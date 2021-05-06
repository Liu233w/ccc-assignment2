<template>
  <v-container>
    <v-row>
      <v-col cols="12">
<!--        <GoogleMapLoader :api-key="mapToken" :mapConfig="mapConfig">-->
<!--          <template v-slot:default="{ google, map }">-->
<!--            <GoogleMapMarker-->
<!--                v-for="marker in markers"-->
<!--                :key="marker.id"-->
<!--                :marker="marker"-->
<!--                :google="google"-->
<!--                :map="map"-->
<!--            />-->
<!--          </template>-->
<!--        </GoogleMapLoader>-->
        <GmapMap
            :center="{lat:10, lng:10}"
            :zoom="7"
            map-type-id="terrain"
            style="width: 500px; height: 300px"
        >
          <GmapMarker
              :key="index"
              v-for="(m, index) in markers"
              :position="m.position"
              :clickable="true"
              :draggable="true"
              @click="center=m.position"
          />
        </GmapMap>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import GoogleMapLoader from "@/components/GoogleMapLoader";
// import GoogleMapMarker from "@/components/GoogleMapMarker";
import {mapSettings} from "@/utils/mapSettings";

export default {
  name: "Map",
  // components: {
  //   GoogleMapLoader,
  //   // GoogleMapMarker
  // },

  data() {
    return {
      markers: [
        {
          id: "a",
          position: { lat: 3, lng: 101 }
        },
        {
          id: "b",
          position: { lat: 5, lng: 99 }
        },
        {
          id: "c",
          position: { lat: 6, lng: 97 }
        }
      ],
      mapCenter: {
        lat: -37.840935,
        lng: 144.946457
      }
    }
  },

  computed: {
    mapToken() {
      return this.$store.state.googleMap.token
    },
    mapConfig() {
      return {
        ...mapSettings,
        center: this.mapCenter
      }
    }
  },

  methods: {

  },

  created() {
  }
}
</script>

<style scoped>

</style>