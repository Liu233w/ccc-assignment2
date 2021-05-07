<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <GmapMap :options="mapConfig" :center="center" class="google-map">
          <GmapInfoWindow
              :options="infoOptions"
              :position="infoWindowPos"
              :opened="infoWinOpen"
              @closeclick="infoWinOpen=false"
              class="info-window"
          >
            <Chart/>
          </GmapInfoWindow>
          <GmapPolygon
              v-for="(r, i) in regions"
              :key="i"
              :paths="r.path"
              :editable="true"
              @click="toggleInfoWindow(r)"/>
          <!--                       @paths_changed="updateEdited($event)"-->
          <!--          />-->
        </GmapMap>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import GoogleMapLoader from "@/components/GoogleMapLoader";
// import GoogleMapMarker from "@/components/GoogleMapMarker";
import Chart from "@/components/Chart";

export default {
  name: "Map",
  components: {
    Chart
  },

  data() {
    return {
      // User's current location
      location: null,

      regions: [
        {
          id: 1,
          name: "City",
          position: {lat: -37.728743, lng: 144.95226},
          path: [
            {lat: -37.685788, lng: 144.890531},
            {lat: -37.685788, lng: 145.013989},
            {lat: -37.771697, lng: 145.013989},
            {lat: -37.771697, lng: 144.890531}
          ]
        },
        {
          id: 2,
          name: "Carlton",
          position: {lat: -37.842533, lng: 145.077912},
          path: [
            {lat: -37.830673, lng: 145.055752},
            {lat: -37.830673, lng: 145.100077},
            {lat: -37.854393, lng: 145.100077},
            {lat: -37.854393, lng: 145.055752}
          ]
        }
      ],

      // Gmap
      center: {
        lat: -37.840935,
        lng: 144.946457
      },

      //  Info Window
      infoOptions: {
        //optional: offset infowindow so it visually sits nicely on top of our marker
        pixelOffset: {
          width: 0,
          height: -35
        }
      },
      infoWindowPos: null,
      infoWinOpen: false,
    }
  },

  computed: {
    mapToken() {
      return this.$store.state.googleMap.token
    },
    mapConfig() {
      return this.$store.state.googleMap.options
    }
  },

  methods: {

    getCurrentLocation() {
      console.log('1')
      if (navigator.geolocation) {
        console.log('geo')
        navigator.geolocation.getCurrentPosition(
            (position) => {
              this.location = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
              };
              this.infoWinOpen = true;
            },
            () => {
              alert("Error: The Geolocation service failed.")
            }
        );
      } else {
        // Browser doesn't support Geolocation
        alert("Error: Your browser doesn't support geolocation.")
      }
    },

    toggleInfoWindow: function (region) {
      this.infoWindowPos = region.position;
      this.infoWinOpen = true
    }
  },

  created() {
  },

  mounted() {

    this.getCurrentLocation()
    // this.setInfoWindowContent()

  }

}
</script>

<style scoped>
.google-map {
  width: 100%;
  height: 650px;
}

.info-window {
  width: 150px;
  height: 200px;
}
</style>