<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <GmapMap :options="mapConfig" :center="center" class="google-map" ref="mapRef">

          <!--          <GmapAutocomplete-->
          <!--              placeholder="This is a placeholder text"/>-->
          <!--&lt;!&ndash;              @place_changed="setPlace"&ndash;&gt;-->

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
              :editable="false"
              @click="toggleInfoWindow(r)"/>
          <!--          <GmapMarker v-for="(m,i) in markers" :key="i" :position="m.position" :clickable="true" :draggable="true" @click="center=m.position"/>-->
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
import {getAllPolygons} from "@/utils/getPolygons.js"

// eslint-disable-next-line no-unused-vars

export default {
  name: "Map",
  components: {
    Chart
  },

  data() {
    return {
      // User's current location
      location: null,
      regions:  [],

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

      // Marker
      markers: [{
        position: this.center
      }]
    }
  },

  computed: {
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

    toggleInfoWindow(region) {
      this.infoWindowPos = region.region_center;
      this.infoWinOpen = true
    },

    handleMarkerClick() {

    }
  },

  created() {
    this.regions = getAllPolygons()
  },

  async mounted() {

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