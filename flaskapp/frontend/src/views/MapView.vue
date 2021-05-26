<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-alert border="right" color="teal darken-3" dark>
          Please select a region and click on it to visualize the result.
        </v-alert>
      </v-col>
      <v-col cols="12">
        <GmapMap
          :options="mapConfig"
          :center="center"
          class="google-map"
          ref="mapRef"
        >
          <template #visible>
            <v-container>
              <v-row>
                <v-col cols="4">
                  <GmapAutocomplete>
                    <template v-slot:input>
                      <v-text-field
                        outlined
                        background-color="#F5F5F5"
                        placeholder="Locations(Split by ',')"
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
            @closeclick="infoWinOpen = false"
            class="info-window"
          >
            <p v-if="loading">Loading...</p>
            <Chart v-else :rename="this.region_onClick" />
          </GmapInfoWindow>

          <GmapPolygon
            v-for="(r, i) in regions"
            :key="i"
            :paths="r.path"
            :options="{ ...polygon_options, ...extra_options[r.name] }"
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
import { getAllPolygons, getPolygonsByNames } from "@/utils/getPolygons.js";

// eslint-disable-next-line no-unused-vars

export default {
  name: "Map",
  components: {
    Chart,
  },

  data() {
    return {
      // User's interaction
      user_input: null,
      region_onClick: null,
      region_onHover: null,

      // Suburbs
      regions: [],

      // Gmap
      center: {
        lat: -37.840935,
        lng: 144.946457,
      },

      //  Info Window
      infoOptions: {
        //optional: offset infowindow so it visually sits nicely on top of our marker
        pixelOffset: {
          width: 0,
          height: -35,
        },
      },
      infoWindowPos: null,
      infoWinOpen: false,

      // Polygons
      polygon_options: {
        visible: true,
        strokeColor: "#FF5722",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: "#FF5722",
        fillOpacity: 0,
      },
      extra_options: {},

      // Marker
      markers: [
        {
          position: this.center,
        },
      ],

      // Loading data
      loading: true,
    };
  },

  computed: {
    mapConfig() {
      return this.$store.state.googleMap.options;
    },
  },

  methods: {
    toggleInfoWindow(region) {
      this.infoWindowPos = region.region_center;
      this.infoWinOpen = true;
      this.region_onClick = region.name;
    },

    togglePolygon(r, flag) {
      if (flag === true) {
        this.$set(this.extra_options, r.name, {
          fillOpacity: 0.4,
        });
      } else {
        this.$delete(this.extra_options, r.name);
      }
    },

    queryLocation() {
      // Todo: User Input Regularization. Default is splitted by ','
      // names is an arrays
      if (!this.user_input) {
        this.regions = getAllPolygons();
        return;
      }

      this.infoWinOpen = false;
      const names = this.user_input.split(",");
      const regions = getPolygonsByNames(names);
      console.log(regions);
      if (regions.length === 0) {
        alert("Location is not found! Please refresh the page!");
      } else {
        this.regions = regions;
      }
      this.polygon_options.visible = true;
    },
  },

  async created() {
    this.regions = getAllPolygons();
    // console.log(getAllPolygons())
    await this.$store.dispatch("categories/refresh");
    this.loading = false;

    this.$store.dispatch("categories/startAutoRefreshing")
  },

  mounted() {
    // this.setInfoWindowContent()
  },
};
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