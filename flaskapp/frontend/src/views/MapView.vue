<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <GmapMap :options="mapConfig" :center="center" class="google-map" ref="mapRef">

          <template #visible>
            <v-container>
              <v-row>
                <v-col cols="4">
                  <GmapAutocomplete>
                    <template v-slot:input>
                      <v-text-field outlined
                                    background-color="#F5F5F5"
                                    placeholder="Locations"
                                    append-icon="mdi-map-marker"
                                    ref="input"
                                    v-model="user_input"
                                    @keydown.enter.native="queryLocation"
                      >
                      </v-text-field>
                    </template>
                  </GmapAutocomplete>
                </v-col>
              </v-row>
            </v-container>
          </template>

          <GmapInfoWindow
              :options="infoOptions"
              :position="infoWindowPos"
              :opened="infoWinOpen"
              @closeclick="infoWinOpen=false"
              class="info-window"
          >
            <Chart :rename="this.region_onClick"/>
          </GmapInfoWindow>

          <GmapPolygon
              v-for="(r, i) in regions"
              :key="i"
              :paths="r.path"
              :options = "{...polygon_options, ...extra_options[r.name]}"
              @mouseover="togglePolygon(r, true)"
              @mouseout="togglePolygon(r, false)"
              @click="toggleInfoWindow(r)"
          />
        </GmapMap>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import GoogleMapLoader from "@/components/GoogleMapLoader";
// import GoogleMapMarker from "@/components/GoogleMapMarker";
import Chart from "@/components/Chart";
import {getAllPolygons, getPolygonsByNames} from "@/utils/getPolygons.js"

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

      // User's interaction
      user_input: null,
      region_onClick: null,
      region_onHover: null,

      // Suburbs
      regions: [],

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

      // Polygons
      polygon_options: {
        visible: true,
        strokeColor:"#FF5722",
        strokeOpacity:0.8,
        strokeWeight:2,
        fillColor:"#FF5722",
        fillOpacity:0
      },
      extra_options: {},

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
      if (navigator.geolocation) {
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
      this.region_onClick = region.name;
    },

    togglePolygon(r, flag) {
      if (flag === true) {
        this.$set(this.extra_options, r.name, {
          fillOpacity: 0.4,
        })
      }
      else {
        this.$delete(this.extra_options, r.name)
      }
    },

    queryLocation() {
      // Todo: User Input Regularization. Default is splitting by ' '. But Box Hill...?
      // names is an arrays
      this.infoWinOpen = false
      this.regions = []
      const names = this.user_input.split(' ')
      try {
        getPolygonsByNames(names).then(res => this.regions = res)
      } catch (err) {
        console.log(err)
      }
      this.polygon_options.visible = true
    },
  },

  created() {
    this.regions = getAllPolygons()
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

.input-box {
  width: 100%;
  height: 40px;
}
</style>